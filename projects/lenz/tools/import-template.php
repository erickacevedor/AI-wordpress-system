<?php
/**
 * Import a built Theme Builder part (header / footer) into the Elementor library
 * and apply it site-wide.
 *
 * Run:  wp eval-file projects/lenz/tools/import-template.php <path.json> <slug>
 *
 * The template `type` is read from the JSON wrapper, so the same command handles
 * header and footer. Display conditions are set to `include/general` — the
 * "Entire Site" condition — which is the step people forget: without it the
 * template exists in the library, imports cleanly, and never appears on the site.
 *
 * Idempotent: re-running against the same slug updates in place.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

$json_path = $args[0] ?? '';
$slug      = $args[1] ?? '';

if ( ! $json_path || ! file_exists( $json_path ) ) {
	WP_CLI::error( 'JSON not found: ' . $json_path );
}

$doc = json_decode( file_get_contents( $json_path ), true );
if ( ! is_array( $doc ) || empty( $doc['content'] ) ) {
	WP_CLI::error( 'No `content` array in ' . $json_path );
}

$type = $doc['type'] ?? '';
if ( ! in_array( $type, array( 'header', 'footer' ), true ) ) {
	WP_CLI::error( 'Unsupported template type: ' . $type );
}

$slug  = $slug ?: ( 'lenz-' . $type );
$title = $doc['title'] ?? ( 'Lenz ' . ucfirst( $type ) );

$existing = get_posts( array(
	'post_type'      => 'elementor_library',
	'name'           => $slug,
	'post_status'    => 'any',
	'posts_per_page' => 1,
) );

$postarr = array(
	'post_title'  => $title,
	'post_name'   => $slug,
	'post_status' => 'publish',
	'post_type'   => 'elementor_library',
);

if ( $existing ) {
	$postarr['ID'] = $existing[0]->ID;
	$tpl_id = wp_update_post( $postarr, true );
	$verb = 'updated';
} else {
	$tpl_id = wp_insert_post( $postarr, true );
	$verb = 'created';
}
if ( is_wp_error( $tpl_id ) ) {
	WP_CLI::error( $tpl_id->get_error_message() );
}

update_post_meta( $tpl_id, '_elementor_data', wp_slash( wp_json_encode( $doc['content'] ) ) );
update_post_meta( $tpl_id, '_elementor_edit_mode', 'builder' );
update_post_meta( $tpl_id, '_elementor_template_type', $type );

/* The library taxonomy is what makes Elementor treat this as a Theme Builder part
   rather than a loose saved template. */
wp_set_object_terms( $tpl_id, $type, 'elementor_library_type' );

/* "Entire Site". Without this the part is built but never displayed. */
update_post_meta( $tpl_id, '_elementor_conditions', array( 'include/general' ) );

if ( class_exists( '\ElementorPro\Modules\ThemeBuilder\Module' ) ) {
	// Rebuild the conditions cache, or the new part will not be picked up until
	// something else happens to invalidate it.
	$tb = \ElementorPro\Modules\ThemeBuilder\Module::instance();
	if ( method_exists( $tb, 'get_conditions_manager' ) ) {
		$cm = $tb->get_conditions_manager();
		if ( method_exists( $cm, 'get_cache' ) ) {
			$cm->get_cache()->regenerate();
		}
	}
}

if ( class_exists( '\Elementor\Plugin' ) ) {
	\Elementor\Plugin::$instance->files_manager->clear_cache();
}

WP_CLI::log( sprintf( '%s %s template #%d (%s) — %d top-level, condition: entire site',
	$verb, $type, $tpl_id, $slug, count( $doc['content'] ) ) );
