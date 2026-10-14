<?php
/**
 * Plugin Name:       Lenz Core
 * Description:       Design system, icon sprite, service CPT and custom widgets for Lenz Heating & Cooling. Everything the Elementor kit cannot carry on its own.
 * Version:           0.2.0
 * Requires at least: 6.7
 * Requires PHP:      7.4
 * Author:            Lenz
 * Text Domain:       lenz-core
 *
 * WHY A PLUGIN AND NOT A CHILD THEME
 * ----------------------------------
 * The design depends on CSS that Elementor's UI cannot express (background-clip:text,
 * stacked radial gradients, mask-image, pseudo-element sheens) plus a service CPT and
 * custom widgets. Putting all of it here rather than in a child theme means:
 *   - it survives a theme switch, and
 *   - the deliverable is TWO artifacts (this plugin + the kit) instead of three.
 *
 * INSTALL ORDER MATTERS: activate this plugin BEFORE importing the kit. Import the kit
 * first and every custom widget renders as "widget not found" and every CSS-owned
 * gradient renders flat.
 */

defined( 'ABSPATH' ) || exit;

define( 'LENZ_CORE_VERSION', '0.2.0' );
define( 'LENZ_CORE_FILE', __FILE__ );
define( 'LENZ_CORE_PATH', plugin_dir_path( __FILE__ ) );
define( 'LENZ_CORE_URL', plugin_dir_url( __FILE__ ) );

/**
 * Master stylesheet.
 *
 * Priority 20 so it lands after the theme and after Elementor's own frontend CSS.
 * That ordering is a safety net, not the mechanism — the actual rule is that we never
 * set a property in a widget that the stylesheet also owns, so there is nothing to
 * fight. See assets/css/lenz-core.css.
 *
 * Version is filemtime(), which permanently solves the manual `?v=` cache-buster the
 * static build had to hand-bump across five HTML files on every deploy.
 */
function lenz_core_enqueue_assets() {
	$css = LENZ_CORE_PATH . 'assets/css/lenz-core.css';

	// The prototype's exact font request. Only these weights exist, so text set
	// at 600 in Montserrat renders the way the approved design shows it.
	wp_enqueue_style(
		'lenz-fonts',
		'https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Open+Sans:wght@400;600;700&display=swap',
		array(),
		null
	);

	wp_enqueue_style(
		'lenz-core',
		LENZ_CORE_URL . 'assets/css/lenz-core.css',
		array(),
		file_exists( $css ) ? filemtime( $css ) : LENZ_CORE_VERSION
	);
}
add_action( 'wp_enqueue_scripts', 'lenz_core_enqueue_assets', 20 );

/**
 * Elementor would otherwise request every weight of the kit's fonts (Montserrat
 * 100 to 900), which both costs a round of downloads and renders the design's
 * 600-weight labels lighter than the approved prototype. lenz-core owns fonts.
 */
add_filter( 'elementor/frontend/print_google_fonts', '__return_false' );

/**
 * Front-end behaviour, ported from the v6-1 prototype's lenz.js: sticky-nav
 * state, the Services mega menu, the mobile menu and its accordion, the FAQ
 * disclosure and the brand marquee loop. See assets/js/lenz-site.js.
 *
 * Front end only: inside the Elementor editor these handlers would fight the
 * canvas's own click handling. Deferred, because none of it is needed before
 * paint.
 */
function lenz_core_enqueue_site_js() {
	$js = LENZ_CORE_PATH . 'assets/js/lenz-site.js';
	if ( ! file_exists( $js ) ) {
		return;
	}

	wp_enqueue_script(
		'lenz-site',
		LENZ_CORE_URL . 'assets/js/lenz-site.js',
		array(),
		filemtime( $js ),
		array( 'strategy' => 'defer', 'in_footer' => true )
	);
}
add_action( 'wp_enqueue_scripts', 'lenz_core_enqueue_site_js', 20 );

/**
 * Inject the Lucide-geometry icon sprite once per page.
 *
 * The sprite is 24 <symbol> definitions referenced as <use href="#i-name"/>. Inlining
 * it (rather than linking the file) is what lets `stroke="currentColor"` inherit the
 * surrounding text colour — which is how the contrast rules in KIT-ANALYSIS.md hold:
 * an eyebrow that passes 4.5:1 with a black icon beside it still fails the user.
 */
function lenz_core_inject_sprite() {
	$sprite = LENZ_CORE_PATH . 'assets/icons/lenz-sprite.svg';

	if ( ! file_exists( $sprite ) ) {
		return;
	}

	// Not esc_html'd on purpose: this is a trusted, version-controlled asset that must
	// render as markup. It contains no dynamic input.
	echo file_get_contents( $sprite ); // phpcs:ignore WordPress.Security.EscapeOutput
}
add_action( 'wp_body_open', 'lenz_core_inject_sprite', 5 );

/**
 * Elementor gets its own copy inside the editor iframe, otherwise every icon in the
 * canvas renders as an empty box while it renders fine on the front end — which reads
 * as "the build is broken" to whoever is editing.
 */
function lenz_core_editor_sprite() {
	lenz_core_inject_sprite();
}
add_action( 'elementor/editor/wp_head', 'lenz_core_editor_sprite' );

/**
 * The stylesheet must also load inside the Elementor editor canvas, or CSS-owned
 * gradients (lead cards, clipped headings) look absent while editing and someone
 * "helpfully" sets a background that then fights the class.
 */
add_action( 'elementor/editor/after_enqueue_styles', 'lenz_core_enqueue_assets' );
add_action( 'elementor/preview/enqueue_styles', 'lenz_core_enqueue_assets' );

/* -------------------------------------------------------------------------
 * Custom Elementor widgets
 *
 * These are the pieces Elementor cannot express with its own widgets. A page
 * importing them renders "widget not found" if this plugin is inactive — which is
 * why the install order in the handoff is plugin FIRST, then kit.
 * ---------------------------------------------------------------------- */
function lenz_core_register_widgets( $widgets_manager ) {
	$widgets = array(
		'class-marquee-widget.php' => 'Lenz_Marquee_Widget',
	);

	foreach ( $widgets as $file => $class ) {
		$path = LENZ_CORE_PATH . 'includes/widgets/' . $file;
		if ( ! file_exists( $path ) ) {
			continue;
		}
		require_once $path;
		if ( class_exists( $class ) ) {
			$widgets_manager->register( new $class() );
		}
	}
}
add_action( 'elementor/widgets/register', 'lenz_core_register_widgets' );

/* -------------------------------------------------------------------------
 * Modules
 * ---------------------------------------------------------------------- */
foreach ( array( 'cpt-service.php' ) as $lenz_module ) {
	$lenz_module_path = LENZ_CORE_PATH . 'includes/' . $lenz_module;
	if ( file_exists( $lenz_module_path ) ) {
		require_once $lenz_module_path;
	}
}
