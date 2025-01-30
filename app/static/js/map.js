document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map').setView([42.320339177381065, 69.59195137023927], 16);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    var marker;

    function onMapClick(e) {
        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker(e.latlng).addTo(map);
        document.getElementById("coords").value = e.latlng.lat + ", " + e.latlng.lng;
    }

    map.on('click', onMapClick);
});
