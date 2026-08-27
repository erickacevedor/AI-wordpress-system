<?php
/**
 * Import a built Theme Builder part (header / footer) into the Elementor library and
 * apply it site-wide. Site-agnostic.
 *
 * Run:  wp eval-file scripts/import-template.php <path.json> [slug] [title]
 *
 * The template `type` is read from the JSON wrapper, so one command handles header and
 * footer. Slug and title default to the document's own title.
 *
 * Display conditions are set to `include/general` -- the "Entire Site" condition --
 * which is the step people forget: without it the template exists in the library,
 * imports cleanly, and never appears on the site.
 *
 * Like scripts/import-page.php, this is aimed at a local verification sandbox; the
 * client's install usually is not reachable from here.
 *
 * Idempotent: re-running against the same slug updates it in place.
 *
 * Requires Elementor Pro on the target -- Theme Builder is a Pro feature.
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

/* Default the slug and title off the document rather than any one site's naming. */
$title = $args[2] ?? ( $doc['title'] ?? ucfirst( $type ) );
$slug  = $slug ?: sanitize_title( $title );

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

/* Re-resolve the document, bypassing Elementor's instance cache.
   -------------------------------------------------------------------------------
   Without this, the FIRST import of a theme part silently produces a conditions
   cache that does not contain it. The template is created, published, has the right
   type meta, the right taxonomy term and the right conditions -- and never renders.

   The cause is an ordering trap, verified on Elementor 4.2.3 / Pro 4.2.2:

     1. wp_insert_post() fires save_post, and something on that hook asks
        Documents_Manager for a document for the brand-new id.
     2. At that instant `_elementor_template_type` has not been written yet, so
        get_doc_type_by_id() falls through to the post-type map and resolves
        `elementor_library` to a LOOP document. Documents_Manager caches that
        instance against the post id.
     3. We then write the meta, the term and the conditions -- all correct.
     4. Conditions_Cache::regenerate() calls documents->get( $id ), gets the CACHED
        Loop instance back, asks it for get_location(), receives '' -- and skips the
        template, because add() only records documents that report a location.

   Clearing the post/term object caches does NOT help: the stale thing is the
   document OBJECT, not the post row. Passing $from_cache = false rebuilds it from
   the meta we just wrote and replaces the cached instance, after which regenerate()
   sees the part correctly.

   The tell, if this ever regresses: the second import of ANY part fixes the first
   one by accident, because by then the bad instance is gone with the request. */
if ( class_exists( '\Elementor\Plugin' ) ) {
	\Elementor\Plugin::$instance->documents->get( $tpl_id, false );
}

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
