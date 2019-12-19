var apiURI = "/api/v1/";
var keyword = "";
var radius = 5000;
var markerClicked = false;

var container = document.getElementById("map");
var options = {
  center: new kakao.maps.LatLng(37.55685146, 127.0431892),
  level: 3
};

var map = new kakao.maps.Map(container, options);
var currentMarkerType = "hospital";
var markers = [];

function addMarker(data, flag) {
  // 마커 생성
  var marker = new kakao.maps.Marker({
    map: map, // 마커를 표시할 지도
    position: new kakao.maps.LatLng(data["lat"], data["lon"]), // 마커를 표시할 위치
    clickable: true,
    name: data["name"] // 마커의 이름
  });

  // 마커에 표시할 인포윈도우를 생성
  if (flag === true) {
    var overlay = new kakao.maps.CustomOverlay({
      content: makeCustomOverlayContent(data),
      map: map,
      position: marker.getPosition()
    });
  }
  // 마커에 mouseover 이벤트와 mouseout 이벤트를 등록합니다
  // 이벤트 리스너로는 클로저를 만들어 등록합니다
  // for문에서 클로저를 만들어 주지 않으면 마지막 마커에만 이벤트가 등록됩니다
  else {
    var infowindow = new kakao.maps.InfoWindow({
      content: makeInfoWindowContent(data) // 인포윈도우에 표시할 내용
    });
    kakao.maps.event.addListener(
      marker,
      "mouseover",
      makeOverListener(map, marker, infowindow)
    );
    kakao.maps.event.addListener(
      marker,
      "mouseout",
      makeOutListener(infowindow)
    );
    // 마커에 click 이벤트를 등록합니다
    var id = data["id"];
    kakao.maps.event.addListener(marker, "click", function() {
      infowindow.close();
      markerClicked = true;
      setMarkerByID(id);
    });
  }
  return marker;
}

function makeCustomOverlayContent(data) {
  var content = "";
}

function makeInfoWindowContent(data) {
  var content = "<div class='card' style='width: 18rem'>";
  content += "<div class='card-body'>";
  content += "<h5 class='card-title'>" + data["name"] + "</h5>";
  content += "<h6 class='card-subtitle text-muted'>" + data["addr"] + "</h6>";
  content += "</div>";
  content += "</div>";
  return content;
}

function deleteMarkers() {
  while (markers.length > 0) {
    var marker = markers.pop();
    marker.setMap(null);
  }
}

function setMarkerByID(id) {
  deleteMarkers();
  var endPoint = "";
  if (currentMarkerType === "hospital") endPoint = "hospitals/";
  else endPoint = "shops/";
  $.ajax(apiURI + endPoint + id).done(function(data) {
    // console.log(element);
    var marker = addMarker(data, true);
    map.setCenter(marker.getPosition());
    setDraggable(false);
    markers.push(marker);
  });
}

function setMarkers() {
  deleteMarkers();
  var position = map.getCenter();
  var endPoint = "";
  if (currentMarkerType === "hospital") endPoint = "hospitals/";
  else endPoint = "shops/";
  $.ajax(apiURI + endPoint, {
    type: "GET",
    data: {
      q: keyword,
      lat: position.getLat(),
      lon: position.getLng(),
      radius: radius
    }
  }).done(function(data) {
    data.forEach(function(element) {
      var marker = addMarker(element, false);
      markers.push(marker);
    });
  });
}

kakao.maps.event.addListener(map, "tilesloaded", function() {
  if (markerClicked === true) return;
  setMarkers();
});

function setDraggable(draggable) {
  // 마우스 드래그로 지도 이동 가능여부를 설정합니다
  map.setDraggable(draggable);
}

// 인포윈도우를 표시하는 클로저를 만드는 함수입니다
function makeOverListener(map, marker, infowindow) {
  return function() {
    infowindow.open(map, marker);
  };
}

// 인포윈도우를 닫는 클로저를 만드는 함수입니다
function makeOutListener(infowindow) {
  return function() {
    infowindow.close();
  };
}

function setMarkerType(markerType) {
  var hospitalBtn = document.getElementById("btn-hospital");
  var shopBtn = document.getElementById("btn-shop");
  if (markerType === "hospital") {
    if (hospitalBtn.classList.contains("active")) return;
    hospitalBtn.classList.replace("btn-secondary", "btn-primary");
    hospitalBtn.classList.add("active");
    hospitalBtn.toggleAttribute("aria-pressed");
    shopBtn.classList.replace("btn-primary", "btn-secondary");
    shopBtn.classList.remove("active");
    shopBtn.toggleAttribute("aria-pressed");
    currentMarkerType = "hospital";
  } else {
    if (shopBtn.classList.contains("active")) return;
    shopBtn.classList.replace("btn-secondary", "btn-primary");
    shopBtn.classList.add("active");
    shopBtn.toggleAttribute("aria-pressed");
    hospitalBtn.classList.replace("btn-primary", "btn-secondary");
    hospitalBtn.classList.remove("active");
    hospitalBtn.toggleAttribute("aria-pressed");
    currentMarkerType = "shop";
  }
  setMarkers();
}
