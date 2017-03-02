<?php

if ( ! defined( 'ABSPATH' ) ) exit;

function fm_admin_notices( $notices ) {

	$one_week_support = add_query_arg( array( 'fm_admin_notice_ignore' => 'one_week_support' ) );
	$notices['one_week_support'] = array(
		'title' => __( 'Hey! How\'s It Going?', 'form-maker' ),
		'msg' => __( 'Thank you for using WordPress Form Maker! We hope that you\'ve found everything you need, but if you have any questions:', 'form-maker' ),
		'link' => '<li><span class="dashicons dashicons-media-text"></span><a target="_blank" href="https://web-dorado.com/wordpress-form-maker/installing.html">' . __( 'Check out User Guide', 'form-maker' ) . '</a></li>
                    <li><span class="dashicons dashicons-sos"></span><a target="_blank" href="https://web-dorado.com/forum/11-form-maker.html">' . __( 'Get Some Help' ,'form-maker' ) . '</a></li>
                    <li><span class="dashicons dashicons-dismiss"></span><a href="' . $one_week_support . '">' . __( 'Never show again' ,'form-maker' ) . '</a></li>',
		'int' => 7
	);

	$two_week_review_ignore = add_query_arg( array( 'fm_admin_notice_ignore' => 'two_week_review' ) );
	$two_week_review_temp = add_query_arg( array( 'fm_admin_notice_temp_ignore' => 'two_week_review', 'int' => 14 ) );
	$notices['two_week_review'] = array(
		'title' => __( 'Leave A Review?', 'fm_admin_notice' ),
		'msg' => __( 'We hope you\'ve enjoyed using WordPress FormMaker! Would you consider leaving us a review on WordPress.org?', 'fm_admin_notice' ),
		'link' => '<li><span class="dashicons dashicons-external"></span><a href="https://wordpress.org/support/view/plugin-reviews/form-maker?filter=5" target="_blank">' . __( 'Sure! I\'d love to!', 'fm_admin_notice' ) . '</a></li>
					<li> <span class="dashicons dashicons-smiley"></span><a href="' . $two_week_review_ignore . '"> ' . __( 'I\'ve already left a review', 'fm_admin_notice' ) . '</a></li>
                    <li><span class="dashicons dashicons-calendar-alt"></span><a href="' . $two_week_review_temp . '">' . __( 'Maybe Later' ,'fm_admin_notice' ) . '</a></li>
                     <li><span class="dashicons dashicons-dismiss"></span><a href="' . $two_week_review_ignore . '">' . __( 'Never show again' ,'fm_admin_notice' ) . '</a></li>',

		'int' => 14
	);


	return $notices;
}

add_filter( 'fm_admin_notices', 'fm_admin_notices' );

