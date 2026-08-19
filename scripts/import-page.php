<?php
/**
 * Import a built page JSON into a WordPress page, headlessly. Site-agnostic.
 *
 * Run:  wp eval-file scripts/import-page.php <path-to.json> <slug> "<Title>" [template]
 *
 * The Elementor UI route is Templates -> Import Templates -> Insert. This does the
 * same thing without a browser, so a build can be verified against a real Elementor
 * render instead of being eyeballed as JSON.
 *
 * WHERE THIS IS MEANT TO RUN: a local throwaway WordPress + Elementor install, as a
 * verification sandbox. The client's own site usually cannot be reached from here --
 * the deliverable is the JSON file plus its handoff note, and somebody else imports
 * it. Use this to confirm the file renders BEFORE it ships. If you do happen to have
 * access to the target, it works there too.
 *
 * Idempotent -- matched by slug, so re-running updates that page rather than piling
 * up duplicates. That keeps a build -> import -> look -> rebuild loop clean.
 *
 * The page template comes from the document's own `page_settings.template` (sites
 * differ: some pages want `default`, others `elementor_header_footer`), and can be
 * overridden with the 4th argument.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

$json_path = $args[0] ?? '';
$slug      = $args[1] ?? '';
$title     = $args[2] ?? '';
$tpl_arg   = $args[3] ?? '';

if ( ! $json_path || ! file_exists( $json_path ) ) {
	WP_CLI::error( 'JSON not found: ' . $json_path );
}

$doc = json_decode( file_get_contents( $json_path ), true );
if ( ! is_array( $doc ) || empty( $doc['content'] ) ) {
	WP_CLI::error( 'Not a single-page wrapper (no `content` array). Kit-format '
		. 'content/page/<id>.json files are for Import Kit, not this.' );
}

$type = $doc['type'] ?? 'page';
if ( 'page' !== $type ) {
	WP_CLI::error( sprintf(
		'This document is type "%s" -- use scripts/import-template.php for header/footer parts.',
		$type ) );
}

if ( ! $slug ) {
	$slug = sanitize_title( $doc['title'] ?? basename( $json_path, '.json' ) );
}
if ( ! $title ) {
	$title = $doc['title'] ?? ucwords( str_replace( '-', ' ', $slug ) );
}

/* The template the page asks for. Getting this wrong is quiet but visible: a page
   built with its own hero on `elementor_header_footer` shows the theme title too when
   imported as `default`, and vice versa. */
$template = $tpl_arg ?: ( $doc['page_settings']['template'] ?? 'default' );

$existing = get_page_by_path( $slug, OBJECT, 'page' );
$postarr  = array(
	'post_title'   => $title,
	'post_name'    => $slug,
	'post_status'  => 'publish',
	'post_type'    => 'page',
	'post_content' => '',
);
if ( $existing ) {
	$postarr['ID'] = $existing->ID;
	$page_id       = wp_update_post( $postarr, true );
	$verb          = 'updated';
} else {
	$page_id = wp_insert_post( $postarr, true );
	$verb    = 'created';
}
if ( is_wp_error( $page_id ) ) {
	WP_CLI::error( $page_id->get_error_message() );
}

/* wp_slash() matters: _elementor_data is a JSON string full of quotes, and
   update_post_meta() runs the value through wp_unslash() on the way in. Without the
   slash the payload comes back mangled and Elementor silently renders an EMPTY page --
   no error, no warning, just a blank canvas. This is the single most expensive thing
   to rediscover, so it stays commented. */
update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $doc['content'] ) ) );
update_post_meta( $page_id, '_elementor_edit_mode', 'builder' );
update_post_meta( $page_id, '_elementor_template_type', 'wp-page' );
update_post_meta( $page_id, '_wp_page_template', $template );

if ( ! empty( $doc['page_settings'] ) ) {
	update_post_meta( $page_id, '_elementor_page_settings', $doc['page_settings'] );
}

if ( class_exists( '\Elementor\Plugin' ) ) {
	\Elementor\Plugin::$instance->files_manager->clear_cache();
}

WP_CLI::log( sprintf( '%s page #%d (%s) — %d top-level sections, template "%s"',
	$verb, $page_id, $slug, count( $doc['content'] ), $template ) );
WP_CLI::log( 'url: ' . get_permalink( $page_id ) );
