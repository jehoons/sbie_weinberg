jQuery(document).ready(function($){
	//if you change this breakpoint in the style.css file (or _layout.scss if you use SASS), don't forget to update this value as well
	var $L = 1200,
		$menu_navigation = $('#main-nav'),
		$cart_trigger = $('#cl-cart-trigger'),
		$hamburger_icon = $('#cl-hamburger-menu'),
		$lateral_cart = $('#cl-cart'),
		$shadow_layer = $('#cl-shadow-layer');

	//open lateral menu on mobile
	$hamburger_icon.on('click', function(event){
		event.preventDefault();
		//close cart panel (if it's open)
		$lateral_cart.removeClass('speed-in');
		toggle_panel_visibility($menu_navigation, $shadow_layer, $('body'));
	});

	//open cart
	$cart_trigger.on('click', function(event){
		event.preventDefault();
		//close lateral menu (if it's open)
		$menu_navigation.removeClass('speed-in');
		toggle_panel_visibility($lateral_cart, $shadow_layer, $('body'));
	});

	//close lateral cart or lateral menu
	$shadow_layer.on('click', function(){
		$shadow_layer.removeClass('is-visible');
		// firefox transitions break when parent overflow is changed, so we need to wait for the end of the trasition to give the body an overflow hidden
		if( $lateral_cart.hasClass('speed-in') ) {
			$lateral_cart.removeClass('speed-in').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
				$('body').removeClass('overflow-hidden');
			});
			$menu_navigation.removeClass('speed-in');
		} else {
			$menu_navigation.removeClass('speed-in').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
				$('body').removeClass('overflow-hidden');
			});
			$lateral_cart.removeClass('speed-in');
		}
	});

	//move #main-navigation inside header on laptop
	//insert #main-navigation after header on mobile
	move_navigation( $menu_navigation, $L);
	$(window).on('resize', function(){
		move_navigation( $menu_navigation, $L);
		
		if( $(window).width() >= $L && $menu_navigation.hasClass('speed-in')) {
			$menu_navigation.removeClass('speed-in');
			$shadow_layer.removeClass('is-visible');
			$('body').removeClass('overflow-hidden');
		}

	});
	
	
	//로그인 클릭하면.
	$('.cl-btn-inner').click(function(){

		sendMessage("입력이 완료 되었습니다.");
			
	});	
});

function toggle_panel_visibility ($lateral_panel, $background_layer, $body) {
	if( $lateral_panel.hasClass('speed-in') ) {
		// firefox transitions break when parent overflow is changed, so we need to wait for the end of the trasition to give the body an overflow hidden
		$lateral_panel.removeClass('speed-in').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
			$body.removeClass('overflow-hidden');
		});
		$background_layer.removeClass('is-visible');

	} else {
		$lateral_panel.addClass('speed-in').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
			$body.addClass('overflow-hidden');
		});
		$background_layer.addClass('is-visible');
	}
}

function move_navigation( $navigation, $MQ) {
	if ( $(window).width() >= $MQ ) {
		$navigation.detach();
		$navigation.appendTo('header');
	} else {
		$navigation.detach();
		$navigation.insertAfter('header');
	}
}


/* --------------------------------

자체 함수

-------------------------------- */
//안내방송
function sendMessage(msg,val){
	
	//로그인 창에서 뜬다면.
	if($('#cl-login-veil').length){
		var loginTrue = true;
		$('#cl-login-veil').remove();
	}
	
	$("body").append("<div id='cl-message-veil'></div> <div id='cl-message'> <div class='message-title'>안내방송</div> <div class='message-content'> "+msg+" </div> <div class='message-button'><a href='#0' id='messagebutton'>닫기</a></div> </div>");
	$('#messagebutton').focus();
	
	$('#cl-message-veil').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();
		if(loginTrue){
			$("body").append("<div id='cl-login-veil'></div>");
			
			$('#cl-login-veil').click(function(){
				$('#cl-login-veil').remove();
				$('#cl-login').remove();
				$('#cl-form-login').remove();
			});
			
		}
		val.focus();
	});
	
	$('#messagebutton').click(function(){
		$('#cl-message-veil').remove();
		$('#cl-message').remove();
		if(loginTrue){
			$("body").append("<div id='cl-login-veil'></div>");
			
			$('#cl-login-veil').click(function(){
				$('#cl-login-veil').remove();
				$('#cl-login').remove();
				$('#cl-form-login').remove();
			});
		}
		val.focus();
	});
	
}