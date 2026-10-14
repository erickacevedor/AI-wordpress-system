<?php
/**
 * Plugin Name:       HVIA Core
 * Description:       Design system and front-end behaviour for the Heart and Vascular Institute of Alabama landing page (ported from the approved HTML prototype, option 2).
 * Version:           0.1.0
 * Requires at least: 6.7
 * Requires PHP:      7.4
 * Author:            Explore Media
 * Text Domain:       hvia-core
 *
 * Same structure as lenz-core (projects/lenz): the prototype stylesheet is ported
 * into assets/css/hvia-core.css by projects/hvia/tools/port-css.py, and the
 * Elementor pages mirror the prototype's DOM and class names. Without this plugin
 * the pages are structurally intact and visually broken.
 *
 * The repo copy (AI-wordpress-system/projects/hvia/plugin/hvia-core) is the source
 * of truth; deploy-plugin.sh copies it into an install.
 */

defined( 'ABSPATH' ) || exit;

define( 'HVIA_CORE_VERSION', '0.1.0' );
define( 'HVIA_CORE_PATH', plugin_dir_path( __FILE__ ) );
define( 'HVIA_CORE_URL', plugin_dir_url( __FILE__ ) );

/**
 * Fonts (the prototype's exact request) and the ported stylesheet. Priority 20 so it
 * lands after the theme and Elementor's frontend CSS; version = filemtime().
 */
function hvia_core_enqueue_assets() {
	$css = HVIA_CORE_PATH . 'assets/css/hvia-core.css';

	wp_enqueue_style(
		'hvia-fonts',
		'https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Golos+Text:wght@400;500;600&family=Instrument+Serif:ital@0;1&family=Onest:wght@500;600;700&display=swap',
		array(),
		null
	);

	wp_enqueue_style(
		'hvia-core',
		HVIA_CORE_URL . 'assets/css/hvia-core.css',
		array(),
		file_exists( $css ) ? filemtime( $css ) : HVIA_CORE_VERSION
	);
}
add_action( 'wp_enqueue_scripts', 'hvia_core_enqueue_assets', 20 );
add_action( 'elementor/editor/after_enqueue_styles', 'hvia_core_enqueue_assets' );
add_action( 'elementor/preview/enqueue_styles', 'hvia_core_enqueue_assets' );

/** hvia-core owns fonts; Elementor would request every weight of the kit's fonts. */
add_filter( 'elementor/frontend/print_google_fonts', '__return_false' );

/**
 * Hello Elementor's header/footer stylesheet styles `.site-header` / `.site-footer`
 * globally (flex, padding), and the prototype uses those class names on its own
 * header and footer bands. The Theme Builder parts replace Hello's header and footer,
 * so its styles are switched off.
 */
add_filter( 'hello_elementor_header_footer', '__return_false' );

/**
 * Front-end behaviour ported from the prototype's main.js: sticky-header state, the
 * mobile nav, the active-link spy, scroll reveals and the footer year. Front end only
 * (in the editor the handlers would fight the canvas); deferred.
 */
function hvia_core_enqueue_site_js() {
	$js = HVIA_CORE_PATH . 'assets/js/hvia-site.js';
	if ( ! file_exists( $js ) ) {
		return;
	}
	wp_enqueue_script(
		'hvia-site',
		HVIA_CORE_URL . 'assets/js/hvia-site.js',
		array(),
		filemtime( $js ),
		array( 'strategy' => 'defer', 'in_footer' => true )
	);
}
add_action( 'wp_enqueue_scripts', 'hvia_core_enqueue_site_js', 20 );

/**
 * The three surgeons, as members of the clinic entity Rank Math builds (MedicalClinic,
 * `publisher`, set up by tools/site-setup.php). Added to that entity rather than
 * printed as a second JSON-LD block, so the page has one organization. Names and
 * roles as on the page (ClickUp 86bcc5579); `member` because employment is not
 * confirmed.
 */
function hvia_core_schema_members( $data ) {
	if ( ! is_front_page() || empty( $data['publisher'] ) || ! is_array( $data['publisher'] ) ) {
		return $data;
	}
	$surgeons = array(
		array( 'Ralph Redd', 'Vascular and Endovascular Surgeon', 'dr-ralph-redd' ),
		array( 'Richard Tan', 'Vascular Surgeon', 'dr-richard-tan' ),
		array( 'Irwin White-Gittens', 'Vascular Surgeon', 'dr-irwin-white-gittens' ),
	);
	$members = array();
	foreach ( $surgeons as $s ) {
		$person = array(
			'@type'           => 'Person',
			'name'            => $s[0],
			'honorificPrefix' => 'Dr.',
			'honorificSuffix' => 'MD',
			'jobTitle'        => $s[1],
		);
		$img = get_posts( array( 'post_type' => 'attachment', 'post_status' => 'inherit', 'meta_key' => '_hvia_media_key',
			'meta_value' => $s[2], 'posts_per_page' => 1, 'fields' => 'ids' ) );
		if ( $img ) {
			$person['image'] = wp_get_attachment_url( $img[0] );
		}
		$members[] = $person;
	}
	$data['publisher']['member'] = $members;

	// The logo URL is stored as a plain string in Rank Math's options, so a push from the
	// http Local site to the https server keeps `http://` (search-replace swaps only the
	// host). Serve it with the site's own scheme.
	foreach ( array( 'url', 'contentUrl' ) as $k ) {
		if ( ! empty( $data['publisher']['logo'][ $k ] ) ) {
			$data['publisher']['logo'][ $k ] = set_url_scheme( $data['publisher']['logo'][ $k ] );
		}
	}

	// Rank Math's organization builder never adds `telephone`; take it from its own setting.
	$phone = class_exists( '\RankMath\Helper' ) ? \RankMath\Helper::get_settings( 'titles.phone' ) : '';
	if ( $phone && empty( $data['publisher']['telephone'] ) ) {
		$data['publisher']['telephone'] = $phone;
	}
	return $data;
}
add_filter( 'rank_math/json_ld', 'hvia_core_schema_members', 20 );

/**
 * The reveal animations start at opacity 0 and rely on the script. The prototype
 * showed everything when JS was off (`.no-js`); this keeps that fallback.
 */
function hvia_core_noscript_reveals() {
	echo '<noscript><style>.elementor .reveal,.elementor .reveal-load,.elementor .reveal-load .elementor-heading-title{opacity:1!important;transform:none!important;animation:none!important}</style></noscript>' . "\n";
}
add_action( 'wp_head', 'hvia_core_noscript_reveals', 99 );
