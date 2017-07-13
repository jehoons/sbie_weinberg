<?php
/* --------------------------------

module/contact/list.php
연락처 페이지.

-------------------------------- */

//localhost : AIzaSyBlYB78wO_eK7_a0sFfo1Pxk-KKMi4eD8M
//weinberg.kaist.ac.kr : AIzaSyCVGNlTE_Hu8Iw9CYV5EwI7OB845Qv9oAc

//__CL__ 정의 되지 않았다면 false 를 return.
if(!defined('__CL__')) exit();
?>
<div id="cl-content">
	<div id="cl-content-title">Contact</div>

<div id="map" style="width:100%;height:500px"></div>

    <script>
      function initMap() {
        var myLatLng = {lat: 36.37155121, lng: 127.3618721};
        // Create a map object and specify the DOM element for display.
        var map = new google.maps.Map(document.getElementById('map'), {
          center: myLatLng,
          scrollwheel: true,
          zoom: 15
        });

        // Create a marker and set its position.
        var marker = new google.maps.Marker({
          map: map,
          position: myLatLng,
          title: 'SBIE is here.'
        });
      }

    </script>

 <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCVGNlTE_Hu8Iw9CYV5EwI7OB845Qv9oAc&callback=initMap"
        async defer></script>
<pre>    
Tel : +82-42-350-4325 (Professor Office), +82-42-867-4304 (Secretary), +82-42-350-4365/5365 (Laboratory)
Fax : +82-42-350-4310
E-mail : ckh@kaist.ac.kr

Postral Address:
Professor Kwang-Hyun Cho, PhD
Department of Bio and Brain Engineering,
Korea Advanced Institute of Science and Technology (KAIST),
291 Daehakro, Yuseong-gu, Daejeon 305-701, Republic of Korea
</pre>    
</div>

