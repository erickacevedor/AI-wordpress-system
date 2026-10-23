<?php
/**
 * Import every inner page listed in pages/inner/pages.json (built by pages/inner/build.py).
 *
 * Run:  wp eval-file projects/newman-air/tools/import-pages.php projects/newman-air/pages/inner/pages.json [status]
 *
 * Same writes as tools/import-page.php (Elementor data, builder mode, header-footer
 * template, `_newman_core = 1`), plus:
 *   - parent pages: `services/ac-repair` lives under the Services page, as on the old site;
 *   - SEO: Rank Math's own meta keys (rank_math_title, rank_math_description,
 *     rank_math_robots). They do nothing until Rank Math is active, then they apply.
 * Idempotent: a page is matched by its full path and updated in place. It never
 * touches the front page setting. Prints a JSON map key => page ID at the end.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

$manifest_path = $args[0] ?? '';
$status        = $args[1] ?? 'publish';
if ( ! $manifest_path || ! file_exists( $manifest_path ) ) {
	WP_CLI::error( 'Manifest not found: ' . $manifest_path );
}
// The manifest's json paths are relative to the project folder: pages/inner/pages.json -> three levels up.
$base  = dirname( dirname( dirname( $manifest_path ) ) );
$pages = json_decode( file_get_contents( $manifest_path ), true );
$ids   = array();

foreach ( $pages as $p ) {
	$json_path = $base . '/' . $p['json'];
	$doc       = json_decode( file_get_contents( $json_path ), true );
	if ( ! is_array( $doc ) || empty( $doc['content'] ) ) {
		WP_CLI::warning( 'skipped (no content): ' . $p['key'] );
		continue;
	}
	$parent_id = 0;
	if ( $p['parent'] ) {
		$parent = get_page_by_path( $p['parent'], OBJECT, 'page' );
		if ( ! $parent ) {
			WP_CLI::error( 'Parent not imported yet: ' . $p['parent'] . ' (for ' . $p['key'] . ')' );
		}
		$parent_id = $parent->ID;
	}
	$path     = $p['parent'] ? $p['parent'] . '/' . $p['slug'] : $p['slug'];
	$existing = get_page_by_path( $path, OBJECT, 'page' );
	$postarr  = array(
		'post_title'   => $p['title'],
		'post_name'    => $p['slug'],
		'post_status'  => $status,
		'post_type'    => 'page',
		'post_parent'  => $parent_id,
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
		WP_CLI::error( $p['key'] . ': ' . $page_id->get_error_message() );
	}

	update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $doc['content'] ) ) );
	update_post_meta( $page_id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $page_id, '_elementor_template_type', 'wp-page' );
	update_post_meta( $page_id, '_wp_page_template', 'elementor_header_footer' );
	update_post_meta( $page_id, '_newman_core', '1' );
	if ( ! empty( $doc['page_settings'] ) ) {
		update_post_meta( $page_id, '_elementor_page_settings', $doc['page_settings'] );
	}
	if ( $p['seo_title'] ) {
		update_post_meta( $page_id, 'rank_math_title', $p['seo_title'] );
	}
	if ( $p['seo_description'] ) {
		update_post_meta( $page_id, 'rank_math_description', $p['seo_description'] );
	}
	if ( ! empty( $p['robots'] ) ) {
		update_post_meta( $page_id, 'rank_math_robots', array( $p['robots'] ) );
	}
	$ids[ $p['key'] ] = $page_id;
	WP_CLI::log( sprintf( '%s #%d %s', $verb, $page_id, get_permalink( $page_id ) ) );
}

if ( class_exists( '\Elementor\Plugin' ) ) {
	\Elementor\Plugin::$instance->files_manager->clear_cache();
}
WP_CLI::log( 'IDS ' . wp_json_encode( $ids ) );
