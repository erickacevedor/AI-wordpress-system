<?php
/**
 * Plugin Name:       Newman Core
 * Description:       Design system for the new Newman Air site (homepage V2.1 port): stylesheet, fonts, icon sprite and front-end behaviour that the Elementor kit cannot carry.
 * Version:           0.1.0
 * Requires at least: 6.7
 * Requires PHP:      7.4
 * Author:            Explore Media
 * Text Domain:       newman-core
 *
 * SCOPE
 * -----
 * The install also serves the live splash page and Esteban's promo landing pages,
 * which must not change. Everything here is therefore opt-in per page: a page
 * built from the V2.1 design carries the post meta `_newman_core = 1` (set by
 * tools/import-page.php), gets the body class `nw-site`, and only then loads the
 * assets. Every ported rule is scoped to `body.nw-site`.
 */

defined( 'ABSPATH' ) || exit;

define( 'NEWMAN_CORE_VERSION', '0.1.0' );
define( 'NEWMAN_CORE_PATH', plugin_dir_path( __FILE__ ) );
define( 'NEWMAN_CORE_URL', plugin_dir_url( __FILE__ ) );

/**
 * True on a page built from the V2.1 design (and in its Elementor editor).
 */
function newman_core_is_site_page() {
	$id = get_queried_object_id();
	if ( isset( $_GET['elementor-preview'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
		$preview = absint( $_GET['elementor-preview'] ); // phpcs:ignore WordPress.Security.NonceVerification
		// Only for someone who can edit that post: a visitor adding the parameter gets the normal page.
		if ( $preview && current_user_can( 'edit_post', $preview ) ) {
			$id = $preview;
		}
	}
	return $id && '1' === (string) get_post_meta( $id, '_newman_core', true );
}

function newman_core_body_class( $classes ) {
	if ( newman_core_is_site_page() ) {
		$classes[] = 'nw-site';
	}
	return $classes;
}
add_filter( 'body_class', 'newman_core_body_class' );

/**
 * Stylesheet and fonts. Priority 20: after the theme and Elementor's frontend CSS.
 * The version is filemtime(), so a redeploy busts the cache by itself.
 */
function newman_core_enqueue_assets() {
	if ( ! newman_core_is_site_page() ) {
		return;
	}
	$css = NEWMAN_CORE_PATH . 'assets/css/newman-core.css';

	// The prototype's exact font request (Bricolage Grotesque + DM Sans).
	wp_enqueue_style(
		'newman-fonts',
		'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=DM+Sans:opsz,wght@9..40,400..700&display=swap',
		array(),
		null
	);
	wp_enqueue_style(
		'newman-core',
		NEWMAN_CORE_URL . 'assets/css/newman-core.css',
		array(),
		file_exists( $css ) ? filemtime( $css ) : NEWMAN_CORE_VERSION
	);
}
add_action( 'wp_enqueue_scripts', 'newman_core_enqueue_assets', 20 );
add_action( 'elementor/editor/after_enqueue_styles', 'newman_core_enqueue_assets' );
add_action( 'elementor/preview/enqueue_styles', 'newman_core_enqueue_assets' );

/**
 * Front-end behaviour ported from the prototype script: header state, parallax,
 * mobile drawer, count-up, scroll reveals, the Difference slider, the brand
 * marquee loop and the map/city hover. Front end only, deferred.
 */
function newman_core_enqueue_site_js() {
	$js = NEWMAN_CORE_PATH . 'assets/js/newman-site.js';
	// Not in the Elementor canvas: there Elementor owns the DOM (re-renders on
	// every edit) and these handlers would fight it; overrides.css shows the
	// animated blocks in their final state instead.
	if ( ! newman_core_is_site_page() || ! file_exists( $js ) || isset( $_GET['elementor-preview'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
		return;
	}
	wp_enqueue_script(
		'newman-site',
		NEWMAN_CORE_URL . 'assets/js/newman-site.js',
		array(),
		filemtime( $js ),
		array( 'strategy' => 'defer', 'in_footer' => true )
	);
}
add_action( 'wp_enqueue_scripts', 'newman_core_enqueue_site_js', 20 );

/**
 * The prototype's icon sprite, inlined once so `currentColor` reaches the icons.
 * Trusted, version-controlled markup with no dynamic input.
 */
function newman_core_inject_sprite() {
	$sprite = NEWMAN_CORE_PATH . 'assets/icons/newman-sprite.svg';
	if ( newman_core_is_site_page() && file_exists( $sprite ) ) {
		echo file_get_contents( $sprite ); // phpcs:ignore WordPress.Security.EscapeOutput
	}
}
add_action( 'wp_body_open', 'newman_core_inject_sprite', 5 );
add_action( 'elementor/editor/wp_head', 'newman_core_inject_sprite' );

/**
 * Elementor would request the kit's fonts in every weight on these pages;
 * newman-core loads the prototype's own.
 */
add_filter(
	'elementor/frontend/print_google_fonts',
	function ( $print ) {
		return newman_core_is_site_page() ? false : $print;
	}
);
