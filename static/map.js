var map;
var markers = [];
var customOverlays = [];
var allStores = []; // 모든 편의점 저장 배열
var geocoder; // 주소-좌표 변환 객체
var currentBrand = 'all'; // 현재 선택된 브랜드
var positionMarker = null; // 현재 위치 마커
var currentPosition = null; // 현재 위치 좌표
var currentInfowindow = null; // 현재 열린 인포윈도우

// 지도 초기화 함수
function initMap() {
    console.log('지도 초기화 시작');
    
    var container = document.getElementById('map');
    if (!container) {
        console.error('지도 컨테이너를 찾을 수 없습니다');
        return;
    }
    
    var options = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567),
        level: 5 // 지도의 확대 레벨
    };
    
    try {
        map = new kakao.maps.Map(container, options);
        console.log('지도 객체 생성 완료');
        
        // 지오코더 생성
        geocoder = new kakao.maps.services.Geocoder();
        console.log('지오코더 생성 완료');
        
        // 지도 클릭 시 열린 인포윈도우 닫기
        kakao.maps.event.addListener(map, 'click', function() {
            closeInfowindow();
        });
        
        console.log('지도 이벤트 리스너 등록 완료');
    } catch (error) {
        console.error('지도 생성 중 오류:', error);
        container.innerHTML = '<div style="padding:20px;text-align:center;color:red;">지도를 불러올 수 없습니다. 페이지를 새로고침해주세요.</div>';
    }
}

// 인포윈도우 닫기 함수
function closeInfowindow() {
    if (currentInfowindow) {
        currentInfowindow.close();
        currentInfowindow = null;
    }
}

// 스크립트 로드 완료 후 실행
function loadMap() {
    console.log('loadMap 함수 실행됨');
    
    // Kakao API가 로드된 후에 초기화
    if (typeof kakao !== 'undefined' && kakao.maps) {
        console.log('Kakao Maps API 로드 완료');
        
        try {
            initMap();
            console.log('지도 초기화 완료');
            
            // 주소 검색 버튼 이벤트
            document.getElementById('searchButton').addEventListener('click', function() {
                searchAddress();
            });
            
            // 주소 입력 후 엔터키 이벤트
            document.getElementById('address').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchAddress();
                }
            });
            
            // 현재 위치 버튼 이벤트
            document.getElementById('findCurrentButton').addEventListener('click', function() {
                findCurrentLocation();
            });
            
            // 브랜드 버튼 이벤트
            document.getElementById('all-stores').addEventListener('click', function() {
                filterByBrand('all');
            });
            document.getElementById('cu').addEventListener('click', function() {
                filterByBrand('cu');
            });
            document.getElementById('gs25').addEventListener('click', function() {
                filterByBrand('gs25');
            });
            document.getElementById('seven').addEventListener('click', function() {
                filterByBrand('세븐일레븐');
            });
            document.getElementById('emart24').addEventListener('click', function() {
                filterByBrand('이마트24');
            });
            
            console.log('모든 이벤트 리스너 등록 완료');
        } catch (error) {
            console.error('지도 초기화 중 오류:', error);
            document.getElementById('map').innerHTML = '<div style="padding:20px;text-align:center;color:red;">지도 로딩 중 오류가 발생했습니다: ' + error.message + '</div>';
        }
    } else {
        console.log('Kakao Maps API 아직 로드 중...');
        // API가 아직 로드되지 않았으면 잠시 후 다시 시도
        setTimeout(loadMap, 100);
    }
}

// 페이지 로드 완료 시 시작
window.onload = loadMap;

// 주소 검색 함수
function searchAddress() {
    var address = document.getElementById('address').value;
    if (!address) {
        alert('주소를 입력해주세요.');
        return;
    }
    
    // 인포윈도우 닫기
    closeInfowindow();
    
    // 주소로 좌표 검색
    geocoder.addressSearch(address, function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
            var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
            
            // 현재 위치 좌표 저장
            currentPosition = {
                lat: result[0].y,
                lng: result[0].x,
                address: result[0].address_name
            };
            
            // 지도 중심 이동
            map.setCenter(coords);
            
            // 기존 마커 제거
            removeAllMarkers();
            allStores = [];
            
            // 현재 위치 마커 추가
            addPositionMarker(coords);
            
            // 편의점 검색
            searchConvenienceStores(result[0].y, result[0].x);
        } else {
            alert('주소 검색에 실패했습니다. 다시 시도해주세요.');
        }
    });
}

// 현재 위치 찾기
function findCurrentLocation() {
    // 인포윈도우 닫기
    closeInfowindow();
    
    // HTTPS가 아닌 경우 경고 메시지
    if (location.protocol !== 'https:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
        alert('현재 위치 기능은 HTTPS 환경에서만 동작합니다. 주소 검색을 이용해주세요.');
        return;
    }
    
    if (!navigator.geolocation) {
        alert('이 브라우저는 위치 서비스를 지원하지 않습니다.');
        return;
    }
    
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        
        // 현재 위치 좌표 저장
        currentPosition = {
            lat: lat,
            lng: lng
        };
        
        // 좌표를 주소로 변환
        var geocoder = new kakao.maps.services.Geocoder();
        geocoder.coord2Address(lng, lat, function(result, status) {
            if (status === kakao.maps.services.Status.OK) {
                if (result[0].address) {
                    currentPosition.address = result[0].address.address_name;
                }
            }
        });
        
        // 지도 중심 변경
        var currentPos = new kakao.maps.LatLng(lat, lng);
        map.setCenter(currentPos);
        
        // 기존 마커 제거
        removeAllMarkers();
        allStores = [];
        
        // 현재 위치 마커 표시
        addPositionMarker(currentPos);
        
        // 편의점 검색
        searchConvenienceStores(lat, lng);
    }, function(error) {
        console.log('Geolocation error:', error);
        switch(error.code) {
            case error.PERMISSION_DENIED:
                alert('위치 정보 접근이 거부되었습니다. 브라우저 설정에서 위치 정보 접근을 허용해주세요.');
                break;
            case error.POSITION_UNAVAILABLE:
                alert('위치 정보를 사용할 수 없습니다.');
                break;
            case error.TIMEOUT:
                alert('위치 정보 요청이 시간 초과되었습니다.');
                break;
            default:
                alert('위치 정보를 가져올 수 없습니다.');
                break;
        }
    });
}

// 현재 위치 마커 추가
function addPositionMarker(position) {
    if (positionMarker) {
        positionMarker.setMap(null);
    }
    
    // 현재 위치 마커 이미지
    var imageSrc = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iOCIgY3k9IjgiIHI9IjciIGZpbGw9IiNmZjAwMDAiIHN0cm9rZT0iI2ZmZmZmZiIgc3Ryb2tlLXdpZHRoPSIyIi8+CjxjaXJjbGUgY3g9IjgiIGN5PSI4IiByPSIzIiBmaWxsPSIjZmZmZmZmIi8+Cjwvc3ZnPg==',
        imageSize = new kakao.maps.Size(24, 24),
        imageOption = {offset: new kakao.maps.Point(12, 12)};
        
    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);
    
    positionMarker = new kakao.maps.Marker({
        position: position,
        map: map,
        image: markerImage
    });
    
    // 인포윈도우 생성
    var infowindow = new kakao.maps.InfoWindow({
        content: '<div style="padding:8px;font-size:12px;font-weight:bold;color:#333;">📍 현재 위치</div>'
    });
    
    // 마커 클릭 시 인포윈도우 표시/숨김 전환
    kakao.maps.event.addListener(positionMarker, 'click', function() {
        if (currentInfowindow === infowindow) {
            closeInfowindow();
        } else {
            closeInfowindow();
            infowindow.open(map, positionMarker);
            currentInfowindow = infowindow;
        }
    });
}

// 편의점 검색
function searchConvenienceStores(lat, lng) {
    var places = new kakao.maps.services.Places();
    
    var callback = function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
            console.log("편의점 검색 결과:", result);
            // 모든 편의점 저장
            allStores = result;
            
            // 현재 선택된 브랜드로 필터링
            filterByBrand(currentBrand);
        } else {
            console.log("편의점 검색 실패:", status);
            document.getElementById('store-count').innerText = "편의점을 찾을 수 없습니다.";
        }
    };
    
    // CS2는 편의점 카테고리 코드
    places.categorySearch('CS2', callback, {
        location: new kakao.maps.LatLng(lat, lng),
        radius: 5000,  // 5km
        sort: kakao.maps.services.SortBy.DISTANCE
    });
}

// 브랜드별 필터링
function filterByBrand(brand) {
    // 인포윈도우 닫기
    closeInfowindow();
    
    // 브랜드 저장
    currentBrand = brand;
    
    // 기존 편의점 마커 제거
    removeStoreMarkers();
    
    // 브랜드별 필터링
    var filteredStores = [];
    if (brand === 'all') {
        filteredStores = allStores;
        console.log("모든 편의점 표시:", filteredStores.length);
    } else {
        filteredStores = allStores.filter(function(store) {
            var name = store.place_name.toLowerCase();
            if (brand === 'cu') {
                return name.includes('cu') || name.includes('씨유');
            } else if (brand === 'gs25') {
                return name.includes('gs') || name.includes('지에스');
            } else if (brand === '세븐일레븐') {
                return name.includes('세븐') || name.includes('7-eleven') || name.includes('7eleven');
            } else if (brand === '이마트24') {
                return name.includes('이마트') || name.includes('emart');
            }
            return false;
        });
        console.log(brand + " 편의점 필터링 결과:", filteredStores.length);
    }
    
    // 필터링된 편의점 마커 추가
    for (var i = 0; i < filteredStores.length; i++) {
        addStoreMarker(filteredStores[i]);
    }
    
    // 결과 표시
    document.getElementById('store-count').innerText = "🏪 찾은 편의점: " + filteredStores.length + "개";
}

// 브랜드 색상 가져오기
function getBrandColor(placeName) {
    placeName = placeName.toLowerCase();
    if (placeName.includes('cu') || placeName.includes('씨유')) {
        return '#8c21de';
    } else if (placeName.includes('gs') || placeName.includes('지에스')) {
        return '#1e44a0';
    } else if (placeName.includes('세븐') || placeName.includes('7-eleven') || placeName.includes('7eleven')) {
        return '#008348';
    } else if (placeName.includes('이마트') || placeName.includes('emart')) {
        return '#f2a81d';
    }
    return '#888888'; // 기타 브랜드
}

// 길찾기 URL 생성
function getDirectionsUrl(place) {
    // 카카오맵 길찾기 URL 형식
    var url = 'https://map.kakao.com/link/to/' + place.place_name + ',' + place.y + ',' + place.x;
    
    // 출발지가 있으면 추가
    if (currentPosition) {
        // 출발지 주소가 있으면 주소로, 없으면 좌표로 설정
        if (currentPosition.address) {
            url = 'https://map.kakao.com/link/from/' + currentPosition.address + ',' + 
                   currentPosition.lat + ',' + currentPosition.lng + 
                   '/to/' + place.place_name + ',' + place.y + ',' + place.x;
        } else {
            url = 'https://map.kakao.com/link/from/현재위치,' + 
                   currentPosition.lat + ',' + currentPosition.lng + 
                   '/to/' + place.place_name + ',' + place.y + ',' + place.x;
        }
    }
    
    return url;
}

// 편의점 마커 추가
function addStoreMarker(place) {
    var position = new kakao.maps.LatLng(place.y, place.x);
    
    // 커스텀 오버레이 생성
    var color = getBrandColor(place.place_name);
    var content = '<div style="position:absolute;background:' + color + ';border:2px solid #fff;border-radius:50%;width:14px;height:14px;box-shadow:0 2px 4px rgba(0,0,0,0.3);"></div>';
    
    var customOverlay = new kakao.maps.CustomOverlay({
        position: position,
        content: content,
        yAnchor: 1
    });
    
    customOverlay.setMap(map);
    customOverlays.push(customOverlay);
    
    // 클릭 이벤트를 위한 마커 (투명)
    var marker = new kakao.maps.Marker({
        position: position,
        map: map,
        opacity: 0
    });
    
    markers.push(marker);
    
    // 길찾기 링크 생성
    var directionsLink = getDirectionsUrl(place);
    
    // 인포윈도우 생성 (길찾기 버튼 추가)
    var infowindow = new kakao.maps.InfoWindow({
        content: '<div style="padding:10px;font-size:13px;min-width:200px;">' + 
                 '<div style="margin-bottom:5px;"><span class="marker-dot" style="background:' + color + ';width:12px;height:12px;border-radius:50%;display:inline-block;margin-right:5px;"></span><strong>' + place.place_name + '</strong></div>' + 
                 '<div style="margin-bottom:5px;color:#666;font-size:12px;">' + (place.road_address_name || place.address_name) + '</div>' +
                 '<div style="margin-bottom:8px;color:#999;font-size:11px;">📍 거리: 약 ' + Math.round(place.distance) + 'm</div>' +
                 '<div style="text-align:center;">' + 
                 '<a href="' + directionsLink + '" target="_blank" style="text-decoration:none;">' + 
                 '<button style="background-color:#f06292;color:white;border:none;border-radius:15px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:500;">🚗 길찾기</button>' + 
                 '</a></div>' +
                 '</div>'
    });
    
    // 마커 클릭 시 인포윈도우 표시/숨김 전환
    kakao.maps.event.addListener(marker, 'click', function() {
        if (currentInfowindow === infowindow) {
            closeInfowindow();
        } else {
            closeInfowindow();
            infowindow.open(map, marker);
            currentInfowindow = infowindow;
        }
    });
    
    // 커스텀 오버레이 클릭 시 인포윈도우 표시/숨김 전환
    kakao.maps.event.addListener(customOverlay, 'click', function() {
        if (currentInfowindow === infowindow) {
            closeInfowindow();
        } else {
            closeInfowindow();
            infowindow.open(map, marker);
            currentInfowindow = infowindow;
        }
    });
}

// 편의점 마커만 제거
function removeStoreMarkers() {
    // 커스텀 오버레이 제거
    for (var i = 0; i < customOverlays.length; i++) {
        customOverlays[i].setMap(null);
    }
    customOverlays = [];
    
    // 마커 제거
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}

// 모든 마커 제거
function removeAllMarkers() {
    removeStoreMarkers();
    
    if (positionMarker) {
        positionMarker.setMap(null);
        positionMarker = null;
    }
}