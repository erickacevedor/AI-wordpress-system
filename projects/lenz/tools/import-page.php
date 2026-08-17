<?php
/**
 * Import a built page JSON straight into a WordPress page.
 *
 * Run:  wp eval-file projects/lenz/tools/import-page.php <path-to.json> <slug> "<Title>"
 *
 * The Elementor UI route is Templates -> Import Templates -> Insert. This does the
 * same thing headlessly so a build can be verified without clicking through the
 * admin: it writes `_elementor_data` (the `content` array, JSON-encoded) onto a real
 * page and marks it as builder-edited.
 *
 * Idempotent — re-running against the same slug updates that page rather than
 * creating duplicates, so a rebuild-and-recheck loop stays clean.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

list( $json_path, $slug, $title ) = array(
	$args[0] ?? '',
	$args[1] ?? 'home',
	$args[2] ?? 'Home',
);

if ( ! $json_path || ! file_exists( $json_path ) ) {
	WP_CLI::error( 'JSON not found: ' . $json_path );
}

$doc = json_decode( file_get_contents( $json_path ), true );
if ( ! is_array( $doc ) || empty( $doc['content'] ) ) {
	WP_CLI::error( 'Not a single-page wrapper (no `content` array).' );
}

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
	$page_id = wp_update_post( $postarr, true );
	$verb = 'updated';
} else {
	$page_id = wp_insert_post( $postarr, true );
	$verb = 'created';
}
if ( is_wp_error( $page_id ) ) {
	WP_CLI::error( $page_id->get_error_message() );
}

/* wp_slash() matters: _elementor_data is a JSON string full of quotes, and
   update_post_meta runs it through wp_unslash on the way in. Without the slash the
   payload comes back mangled and Elementor silently renders an empty page. */
update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $doc['content'] ) ) );
update_post_meta( $page_id, '_elementor_edit_mode', 'builder' );
update_post_meta( $page_id, '_elementor_template_type', 'wp-page' );
update_post_meta( $page_id, '_wp_page_template', 'elementor_header_footer' );

if ( ! empty( $doc['page_settings'] ) ) {
	update_post_meta( $page_id, '_elementor_page_settings', $doc['page_settings'] );
}

if ( class_exists( '\Elementor\Plugin' ) ) {
	\Elementor\Plugin::$instance->files_manager->clear_cache();
}

WP_CLI::log( sprintf( '%s page #%d (%s) — %d top-level sections', $verb, $page_id, $slug, count( $doc['content'] ) ) );
WP_CLI::log( 'url: ' . get_permalink( $page_id ) );
