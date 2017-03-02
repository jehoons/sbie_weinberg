				<?php 
				
					if( !of_get_option('header_slider') ) {
						
							echo '<div id="feature" class="site-slider"><div class="site-slider-custom-header"><img src="'.get_stylesheet_directory_uri().'/images/custom-header.jpg" /></div></div>';
												
					}else{
						if( of_get_option('header_slider') == 'cheader' ) {
							get_template_part( 'slider', 'cheader' ); 
						}else{
							get_template_part( 'slider', 'one' ); 
						}
					}
				?>