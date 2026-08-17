<?php
/**
 * Push the Lenz design tokens into Elementor's Site Settings (Global Colors + Fonts).
 *
 * Run:  wp eval-file projects/lenz/tools/set-globals.php
 *
 * Elementor stores these on the active KIT post, in `_elementor_page_settings`.
 * Global ids are normally random 7-char strings; we use readable deterministic ones
 * (`lzgold`, `lzcream`, ...) so the references that end up inside page JSON and in
 * tokens.json stay legible and stable across rebuilds.
 *
 * NOTE ON TYPOGRAPHY: these global slots exist for the EDITOR's convenience — so a
 * client picking "Section Heading" gets the right font. Builds still emit explicit
 * per-widget font sizes, because a heading that only points at a global typography
 * slot does NOT shrink on mobile. That is exactly what responsive-audit.py flags.
 *
 * Idempotent: re-running overwrites the same ids rather than appending duplicates.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

$kit_id = (int) get_option( 'elementor_active_kit' );
if ( ! $kit_id ) {
	WP_CLI::error( 'No active Elementor kit found.' );
}

function lz_px( $n )  { return array( 'unit' => 'px', 'size' => $n, 'sizes' => array() ); }
function lz_em( $n )  { return array( 'unit' => 'em', 'size' => $n, 'sizes' => array() ); }

/* -------------------------------------------------------------- COLORS ---- */
/* The four SYSTEM slots are what unstyled widgets fall back to, so they carry the
   roles that appear most: the CTA blue, the dominant navy, body ink, and the
   corrected accent rust (#D6410F — 4.54:1, the body-safe one, NOT orange-500). */
$system_colors = array(
	array( '_id' => 'primary',   'title' => 'Brand Blue (CTA)', 'color' => '#1837BE' ),
	array( '_id' => 'secondary', 'title' => 'Deep Navy',        'color' => '#07113B' ),
	array( '_id' => 'text',      'title' => 'Ink',              'color' => '#121212' ),
	array( '_id' => 'accent',    'title' => 'Accent Rust',      'color' => '#D6410F' ),
);

$custom_colors = array(
	array( '_id' => 'lzcream',   'title' => 'Cream Surface',    'color' => '#FFFCF0' ),
	array( '_id' => 'lzmist',    'title' => 'Mist Surface',     'color' => '#F1F4FD' ),
	array( '_id' => 'lzwhite',   'title' => 'White',            'color' => '#FFFFFF' ),
	/* Gold never carries white text — pair only with Ink. */
	array( '_id' => 'lzgold',    'title' => 'Flame Gold',       'color' => '#FFC600' ),
	array( '_id' => 'lzgold4',   'title' => 'Gold Hover',       'color' => '#FFCF29' ),
	/* Display only — 3.39:1. Never body text. */
	array( '_id' => 'lzorange',  'title' => 'Display Orange',   'color' => '#F05A28' ),
	array( '_id' => 'lzpurple',  'title' => 'Cool Purple',      'color' => '#7B2D8B' ),
	array( '_id' => 'lzpurple6', 'title' => 'Purple 600',       'color' => '#8F34A2' ),
	array( '_id' => 'lzblue5',   'title' => 'Brand Blue 500',   'color' => '#1A3BCC' ),
	array( '_id' => 'lzblue7',   'title' => 'Blue 700',         'color' => '#122A91' ),
	array( '_id' => 'lzblue8',   'title' => 'Blue 800',         'color' => '#0D1D64' ),
	array( '_id' => 'lzraised',  'title' => 'Navy Raised',      'color' => '#0D1A4E' ),
	array( '_id' => 'lzdborder', 'title' => 'Navy Border',      'color' => '#1B2A6B' ),
	array( '_id' => 'lzblue1',   'title' => 'Blue 100 on Dark', 'color' => '#DFE4FB' ),
	array( '_id' => 'lztext2',   'title' => 'Text Secondary',   'color' => '#616161' ),
	array( '_id' => 'lzborder',  'title' => 'Border',           'color' => '#E0E0E0' ),
	array( '_id' => 'lzsuccess', 'title' => 'Success',          'color' => '#1B6E3C' ),
	array( '_id' => 'lzerror',   'title' => 'Error',            'color' => '#B3261E' ),
);

/* ---------------------------------------------------------- TYPOGRAPHY ---- */
$system_typography = array(
	array(
		'_id' => 'primary', 'title' => 'Display (Montserrat 800)',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Montserrat', 'typography_font_weight' => '800',
	),
	array(
		'_id' => 'secondary', 'title' => 'Heading (Montserrat 700)',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Montserrat', 'typography_font_weight' => '700',
	),
	array(
		'_id' => 'text', 'title' => 'Body (Open Sans 400)',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Open Sans', 'typography_font_weight' => '400',
		'typography_line_height' => lz_em( 1.7 ),
	),
	array(
		'_id' => 'accent', 'title' => 'Accent (Montserrat 700)',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Montserrat', 'typography_font_weight' => '700',
	),
);

$custom_typography = array(
	array(
		'_id' => 'lzhero', 'title' => 'Hero H1',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Montserrat', 'typography_font_weight' => '800',
		'typography_font_size' => lz_px( 61 ),
		'typography_font_size_tablet' => lz_px( 48 ),
		'typography_font_size_mobile' => lz_px( 39 ),
		'typography_line_height' => lz_em( 1.02 ),
		'typography_letter_spacing' => lz_em( -0.04 ),
	),
	array(
		'_id' => 'lzh2', 'title' => 'Section H2',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Montserrat', 'typography_font_weight' => '800',
		'typography_font_size' => lz_px( 39 ),
		'typography_font_size_tablet' => lz_px( 33 ),
		'typography_font_size_mobile' => lz_px( 28 ),
		'typography_line_height' => lz_em( 1.15 ),
		'typography_letter_spacing' => lz_em( -0.02 ),
	),
	array(
		'_id' => 'lzh3', 'title' => 'Card H3',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Montserrat', 'typography_font_weight' => '700',
		'typography_font_size' => lz_px( 25 ),
		'typography_font_size_mobile' => lz_px( 21 ),
		'typography_line_height' => lz_em( 1.15 ),
	),
	array(
		'_id' => 'lzlead', 'title' => 'Lead Paragraph',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Open Sans', 'typography_font_weight' => '400',
		'typography_font_size' => lz_px( 20 ),
		'typography_line_height' => lz_em( 1.6 ),
	),
	array(
		'_id' => 'lzeyebrow', 'title' => 'Eyebrow',
		'typography_typography' => 'custom',
		'typography_font_family' => 'Montserrat', 'typography_font_weight' => '700',
		'typography_font_size' => lz_px( 10 ),
		'typography_letter_spacing' => lz_em( 0.14 ),
		'typography_text_transform' => 'uppercase',
	),
);

/* ------------------------------------------------------------- APPLY ------ */
$settings = get_post_meta( $kit_id, '_elementor_page_settings', true );
if ( ! is_array( $settings ) ) {
	$settings = array();
}

$settings['system_colors']      = $system_colors;
$settings['custom_colors']      = $custom_colors;
$settings['system_typography']  = $system_typography;
$settings['custom_typography']  = $custom_typography;

/* The design's locked content width. The builder library boxes every section to the
   same 1140, so a mismatch here would show as sections that do not line up. */
$settings['container_width']    = lz_px( 1140 );
$settings['space_between_widgets'] = lz_px( 0 );

update_post_meta( $kit_id, '_elementor_page_settings', $settings );

/* Elementor caches generated CSS per post; without this the new globals exist in the
   database but the front end keeps serving the old values. */
if ( class_exists( '\Elementor\Plugin' ) ) {
	\Elementor\Plugin::$instance->files_manager->clear_cache();
}

/* Emit the id map so tokens.json can record the global refs. */
$map = array();
foreach ( $system_colors as $c ) { $map[ $c['title'] ] = 'globals/colors?id=' . $c['_id']; }
foreach ( $custom_colors as $c ) { $map[ $c['title'] ] = 'globals/colors?id=' . $c['_id']; }

WP_CLI::log( 'kit_id=' . $kit_id );
WP_CLI::log( 'colors: ' . ( count( $system_colors ) + count( $custom_colors ) )
	. '  typography: ' . ( count( $system_typography ) + count( $custom_typography ) ) );
WP_CLI::log( wp_json_encode( $map, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) );
