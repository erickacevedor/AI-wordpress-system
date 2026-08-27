<?php
/**
 * Mid Lakes — child theme bootstrap.
 *
 * Three jobs, and deliberately nothing else:
 *   1. enqueue the parent stylesheet, then the capped Mid Lakes stylesheet after it
 *   2. enqueue the exact Google Fonts URL the prototype uses — Fraunces rides the
 *      `opsz` VARIABLE axis, which Elementor's font picker cannot express
 *   3. inline the SVG icon sprite once per page so the service-card `html` widgets
 *      can reference its symbols with <use href="#ml-icon-…">
 *
 * The repo is the source of truth. This folder is deployed by
 * projects/midlakes/deploy-theme.sh; editing it inside wp-content/themes/ and
 * expecting the change to persist is the failure mode that script exists to prevent.
 *
 * @package mid-lakes
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'MID_LAKES_VERSION', '1.0.0' );

/**
 * Styles.
 *
 * Order matters. hello-elementor's own `h1 { font-size: … }` sits at specificity
 * (0,0,1); so does nothing in our sheet, because every capped rule is class-scoped.
 * But the parent must still load first so anything we do share a selector with
 * resolves our way on source order.
 */
function mid_lakes_enqueue_styles() {
	wp_enqueue_style(
		'hello-elementor-child-parent',
		get_template_directory_uri() . '/style.css',
		array(),
		MID_LAKES_VERSION
	);

	// Manrope 400–800 + Fraunces italic on the ital,opsz,wght axes. Elementor
	// auto-enqueues Manrope when a widget names it, but it cannot request the
	// Fraunces variable axes — so we ask for the prototype's exact URL.
	wp_enqueue_style(
		'mid-lakes-fonts',
		'https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,500&display=swap',
		array(),
		null
	);

	wp_enqueue_style(
		'mid-lakes',
		get_stylesheet_directory_uri() . '/assets/mid-lakes.css',
		array( 'hello-elementor-child-parent', 'mid-lakes-fonts' ),
		MID_LAKES_VERSION
	);
}
add_action( 'wp_enqueue_scripts', 'mid_lakes_enqueue_styles', 20 );

/**
 * Preconnect to the Google Fonts hosts, the way the prototype's <head> does.
 */
function mid_lakes_resource_hints( $urls, $relation_type ) {
	if ( 'preconnect' === $relation_type ) {
		$urls[] = array( 'href' => 'https://fonts.googleapis.com' );
		$urls[] = array( 'href' => 'https://fonts.gstatic.com', 'crossorigin' );
	}
	return $urls;
}
add_filter( 'wp_resource_hints', 'mid_lakes_resource_hints', 10, 2 );

/**
 * Stop Elementor printing its own Google Fonts request.
 *
 * The site uses exactly two families and mid_lakes_enqueue_styles() already asks
 * for both, at the exact axes they need. Left alone, Elementor adds a SECOND
 * request for Manrope at every weight and every italic — nine faces the design
 * never uses, none of which the prototype loads.
 *
 * ⚠️ The trade: a font this theme does not enqueue will not load. That is fine
 * while the site is Manrope + Fraunces and nothing else. If a third family is
 * ever introduced, add it to the URL above or drop this filter.
 */
add_filter( 'elementor/frontend/print_google_fonts', '__return_false' );

/**
 * Inline the icon sprite at the top of <body>.
 *
 * PORT-DECISIONS decision 4: the six service icons ship as an inline sprite
 * referenced from small `html` widgets, rather than mapped onto an icon font. The
 * sprite is hidden; the widgets do <svg><use href="#ml-icon-wrench"/></svg>.
 *
 * Printed on every front-end view, including the Elementor editor preview, so the
 * icons are visible while the page is being edited.
 */
function mid_lakes_print_icon_sprite() {
	if ( is_admin() ) {
		return;
	}
	$sprite = get_stylesheet_directory() . '/assets/icons.svg';
	if ( is_readable( $sprite ) ) {
		// Local, version-controlled, developer-authored SVG — not user input.
		echo file_get_contents( $sprite ); // phpcs:ignore WordPress.WP.AlternativeFunctions, WordPress.Security.EscapeOutput
	}
}
add_action( 'wp_body_open', 'mid_lakes_print_icon_sprite' );

/**
 * Theme color meta, matching the prototype's <meta name="theme-color" content="#0f1f35">.
 */
function mid_lakes_theme_color_meta() {
	echo '<meta name="theme-color" content="#0f1f35" />' . "\n";
}
add_action( 'wp_head', 'mid_lakes_theme_color_meta' );

/**
 * [ml_year] — the current year, for the footer copyright line.
 *
 * The prototype fills `<span id="year">` from JavaScript. That is the wrong tool
 * here: the footer is a Theme Builder template, Elementor's text-editor widget runs
 * do_shortcode(), and rendering the year server-side means it is correct in the HTML
 * source rather than a frame after paint.
 */
function mid_lakes_year_shortcode() {
	return esc_html( wp_date( 'Y' ) );
}
add_shortcode( 'ml_year', 'mid_lakes_year_shortcode' );
