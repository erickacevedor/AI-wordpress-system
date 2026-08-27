<?php
/**
 * Mid Lakes — set the Elementor Default Kit's BASE TYPOGRAPHY and content width.
 *
 * Why this exists, and why it is deliberately this small:
 *
 * The kit arrived stock, which meant Elementor's built-in defaults applied —
 * Roboto / Roboto Slab. Two consequences, both real:
 *   1. anything that INHERITS (Pro form fields, accordion body copy, list items,
 *      an unstyled text widget someone adds later) rendered in Roboto;
 *   2. every page paid for two Google Fonts requests nobody wanted.
 *
 * Base typography is exactly what the Elementor kit is FOR, so it is set here
 * rather than fought in the child theme's capped stylesheet.
 *
 * COLOURS ARE DELIBERATELY NOT SET. `system_colors` stays stock and every colour
 * stays inline in build.py — see tokens.json's `_note` and the midlakes-* skills.
 * Splitting colour between a kit slot and inline values would create two sources
 * of truth for the one thing this port most needs to get exactly right.
 *
 * Idempotent. Run:  ./wp.sh eval-file tools/set-kit-defaults.php
 */

$kit_id = (int) get_option( 'elementor_active_kit' );
if ( ! $kit_id ) {
	WP_CLI::error( 'No elementor_active_kit option — is Elementor active?' );
}

$settings = get_post_meta( $kit_id, '_elementor_page_settings', true );
if ( ! is_array( $settings ) ) {
	$settings = array();
}

// Manrope is the only face on the site; Fraunces is applied by class from the
// child theme, because its opsz variable axis has no font-picker support.
$settings['system_typography'] = array(
	array(
		'_id'                      => 'primary',
		'title'                    => 'Primary',
		'typography_typography'    => 'custom',
		'typography_font_family'   => 'Manrope',
		'typography_font_weight'   => '800',   // headings are 800 throughout
	),
	array(
		'_id'                      => 'secondary',
		'title'                    => 'Secondary',
		'typography_typography'    => 'custom',
		'typography_font_family'   => 'Manrope',
		'typography_font_weight'   => '700',
	),
	array(
		'_id'                      => 'text',
		'title'                    => 'Text',
		'typography_typography'    => 'custom',
		'typography_font_family'   => 'Manrope',
		'typography_font_weight'   => '400',
	),
	array(
		'_id'                      => 'accent',
		'title'                    => 'Accent',
		'typography_typography'    => 'custom',
		'typography_font_family'   => 'Manrope',
		'typography_font_weight'   => '600',
	),
);

// body { font-family: var(--font-sans); line-height: 1.6 } from the prototype.
$settings['body_typography_typography']  = 'custom';
$settings['body_typography_font_family'] = 'Manrope';
$settings['body_typography_font_weight'] = '400';
$settings['body_typography_line_height'] = array( 'unit' => 'em', 'size' => 1.6, 'sizes' => array() );

// --container: 1200px. build.py sets boxed_width explicitly on every section, so
// this is for the editor's benefit and for anything added by hand later.
$settings['container_width'] = array( 'unit' => 'px', 'size' => 1200, 'sizes' => array() );

/*
 * Turn on the Tablet Extra breakpoint at 1200px.
 *
 * The prototype collapses its primary nav at exactly 1200px, and for a concrete
 * reason recorded in styles.css: seven page links plus the phone number run out of
 * room well before the page grid does. Elementor ships only mobile (767) and tablet
 * (1024) active, and the Nav Menu widget's "Breakpoint" dropdown is populated from
 * whatever breakpoints ARE active — so without this, the header can only collapse at
 * 1024 and the 1025–1200 band stays crowded.
 *
 * This is additive: existing _tablet values still apply at <=1024, _mobile at <=767.
 * Nothing else on the site uses _tablet_extra.
 */
$settings['active_breakpoints']     = array( 'viewport_mobile', 'viewport_tablet', 'viewport_tablet_extra', 'viewport_laptop' );
$settings['viewport_tablet_extra']  = 1200;

/*
 * ...and the Laptop breakpoint at 1400px, for the step BEFORE the collapse.
 *
 * styles.css does not go straight from a full nav to a burger. At 1400px it first
 * TIGHTENS -- gap 28 -> 18, font 0.95rem -> 0.9rem -- because seven links plus the
 * phone number stop fitting comfortably well above the point where they stop fitting
 * at all. Without this breakpoint the nav is over-wide between 1200 and 1400 and
 * wraps onto a second line.
 *
 * Elementor's laptop default is 1366; the prototype's number is 1400, so it is set
 * explicitly rather than left on the default.
 */
$settings['viewport_laptop']        = 1400;

update_post_meta( $kit_id, '_elementor_page_settings', $settings );

// Force the kit CSS to be rebuilt so the font list in _elementor_css is refreshed.
delete_post_meta( $kit_id, '_elementor_css' );

WP_CLI::success( sprintf( 'Kit %d: Manrope base typography, 1200px container, tablet_extra@1200 + laptop@1400. Colours left stock.', $kit_id ) );
