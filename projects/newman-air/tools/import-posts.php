<?php
/**
 * Import the migrated blog posts (content/blog/*.json, from tools/make-blog.py).
 *
 * Run:  wp eval-file projects/newman-air/tools/import-posts.php projects/newman-air/content [author_id]
 *
 * For each post: create or update it by slug (same slug, date and category as on
 * callbestinshow.com), store the clean HTML as post_content, set `_newman_core = 1`
 * (newman-core styles the single-post template) and Rank Math meta. Images come from
 * the local cache content/source/blog-img (map.json: old URL -> file) into the Media
 * Library once: an attachment remembers its old URL in `_newman_src`, so re-runs reuse it.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$dir    = rtrim( $args[0] ?? '', '/' );
$author = (int) ( $args[1] ?? 1 );
$map    = json_decode( file_get_contents( $dir . '/source/blog-img/map.json' ), true );
if ( ! is_array( $map ) ) {
	WP_CLI::error( 'No image map at ' . $dir . '/source/blog-img/map.json' );
}

/** Attachment for an old image URL: reuse, or copy the cached file into the library. */
function newman_attachment_for( $url, $alt, $parent, $map ) {
	$found = get_posts( array( 'post_type' => 'attachment', 'post_status' => 'inherit', 'posts_per_page' => 1,
		'meta_key' => '_newman_src', 'meta_value' => $url, 'fields' => 'ids' ) );
	if ( $found ) {
		return (int) $found[0];
	}
	if ( empty( $map[ $url ] ) || ! file_exists( $map[ $url ] ) ) {
		WP_CLI::warning( 'image not cached: ' . $url );
		return 0;
	}
	$tmp = wp_tempnam( basename( $map[ $url ] ) );
	copy( $map[ $url ], $tmp );
	$id = media_handle_sideload( array( 'name' => basename( $map[ $url ] ), 'tmp_name' => $tmp ), $parent );
	if ( is_wp_error( $id ) ) {
		WP_CLI::warning( $url . ': ' . $id->get_error_message() );
		return 0;
	}
	update_post_meta( $id, '_newman_src', $url );
	if ( $alt ) {
		update_post_meta( $id, '_wp_attachment_image_alt', $alt );
	}
	return (int) $id;
}

$ids = array();
foreach ( glob( $dir . '/blog/*.json' ) as $file ) {
	$p = json_decode( file_get_contents( $file ), true );

	$cat_id = 0;
	if ( $p['category'] ) {
		$term   = term_exists( $p['category'], 'category' ) ?: wp_insert_term( $p['category'], 'category' );
		$cat_id = is_array( $term ) ? (int) $term['term_id'] : (int) $term;
	}
	$existing = get_page_by_path( $p['slug'], OBJECT, 'post' );
	$postarr  = array(
		'post_type'     => 'post',
		'post_status'   => 'publish',
		'post_title'    => $p['title'],
		'post_name'     => $p['slug'],
		'post_date'     => $p['date'],
		'post_excerpt'  => $p['excerpt'],
		'post_author'   => $author,
		'post_category' => $cat_id ? array( $cat_id ) : array(),
		'post_content'  => '',
	);
	if ( $existing ) {
		$postarr['ID'] = $existing->ID;
	}
	$post_id = wp_insert_post( wp_slash( $postarr ), true );
	if ( is_wp_error( $post_id ) ) {
		WP_CLI::error( $p['slug'] . ': ' . $post_id->get_error_message() );
	}

	// Inline images -> library copies.
	$html = $p['html'];
	foreach ( $p['images'] as $url ) {
		$att = newman_attachment_for( $url, '', $post_id, $map );
		if ( $att ) {
			$html = str_replace( $url, wp_get_attachment_url( $att ), $html );
		}
	}
	wp_update_post( wp_slash( array( 'ID' => $post_id, 'post_content' => $html ) ) );

	if ( $p['thumb'] ) {
		$thumb = newman_attachment_for( $p['thumb'], $p['thumb_alt'], $post_id, $map );
		if ( $thumb ) {
			set_post_thumbnail( $post_id, $thumb );
		}
	}
	update_post_meta( $post_id, '_newman_core', '1' );
	foreach ( array( 'rank_math_title' => 'seo_title', 'rank_math_description' => 'seo_description',
		'rank_math_focus_keyword' => 'focus_keyword' ) as $meta => $key ) {
		if ( ! empty( $p[ $key ] ) ) {
			update_post_meta( $post_id, $meta, $p[ $key ] );
		}
	}
	$ids[ $p['slug'] ] = $post_id;
	WP_CLI::log( sprintf( '%s #%d %s', $existing ? 'updated' : 'created', $post_id, get_permalink( $post_id ) ) );
}
WP_CLI::log( 'IDS ' . wp_json_encode( $ids ) );
