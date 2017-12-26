<?php
if(!defined('__CL__')) exit();
?>
<div class="module-upspace"></div>

<div class="module-content-wraper">
	<div id="map" style="width:100%;height:500px;border-bottom: 1px solid #b9b9b9;"></div>
	
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
	
	<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCVGNlTE_Hu8Iw9CYV5EwI7OB845Qv9oAc&callback=initMap" async defer></script>
	
	<div style="padding: 5em 0em 5em 0em; line-height: 25px; width: 100%; font-size: 14px; margin: auto; width:400px;">
	Tel : +82-42-350-4325 (Professor Office), +82-42-867-4304 (Secretary), +82-42-350-4365/5365 (Laboratory)<br />
	Fax : +82-42-350-4310<br />
	E-mail : ckh@kaist.ac.kr<br /><br />
	
	Postral Address:<br />
	Professor Kwang-Hyun Cho, PhD<br />
	Department of Bio and Brain Engineering,<br />
	Korea Advanced Institute of Science and Technology (KAIST),<br />
	291 Daehakro, Yuseong-gu, Daejeon 305-701, Republic of Korea<br />
	</div>
</div>
