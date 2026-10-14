<?php
/**
 * Import the project's images into the WordPress media library and write media.json.
 *
 * Run:  wp eval-file projects/hvia/tools/upload-media.php <media-dir> <media.json>
 *
 * Idempotent: each attachment is tagged with `_hvia_media_key` (the file name without
 * extension), so a re-run reuses the existing attachment instead of uploading a copy.
 * media.json maps key -> {id, url}; brand.py reads it and makes the URLs root-relative.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$dir  = rtrim( $args[0] ?? '', '/\\' );
$out  = $args[1] ?? '';
if ( ! $dir || ! is_dir( $dir ) || ! $out ) {
	WP_CLI::error( 'usage: upload-media.php <media-dir> <media.json>' );
}

$map = array();
foreach ( glob( $dir . '/*.{jpg,jpeg,png,webp,svg}', GLOB_BRACE ) as $file ) {
	$key = pathinfo( $file, PATHINFO_FILENAME );

	$found = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'meta_key'       => '_hvia_media_key',
		'meta_value'     => $key,
		'posts_per_page' => 1,
		'fields'         => 'ids',
	) );

	if ( $found ) {
		$id   = $found[0];
		$verb = 'kept';
	} else {
		// media_handle_sideload moves the file, so hand it a temporary copy.
		$tmp = wp_tempnam( basename( $file ) );
		copy( $file, $tmp );
		$id = media_handle_sideload( array( 'name' => basename( $file ), 'tmp_name' => $tmp ), 0 );
		if ( is_wp_error( $id ) ) {
			@unlink( $tmp );
			WP_CLI::error( $key . ': ' . $id->get_error_message() );
		}
		update_post_meta( $id, '_hvia_media_key', $key );
		$verb = 'uploaded';
	}

	$map[ $key ] = array( 'id' => (int) $id, 'url' => wp_get_attachment_url( $id ) );
	WP_CLI::log( sprintf( '%-8s #%d %s', $verb, $id, $key ) );
}

ksort( $map );
file_put_contents( $out, wp_json_encode( $map, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) . "\n" );
WP_CLI::success( count( $map ) . ' media items -> ' . $out );
