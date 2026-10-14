<?php
/**
 * Site-level setup for the HVIA install: identity, permalinks, Rank Math (SEO meta,
 * Open Graph, MedicalClinic schema), and removal of WordPress's sample content.
 *
 * Run AFTER build-all.sh --import and upload-media.php (it needs page `home` and
 * the media keys in media.json):
 *   wp eval-file projects/hvia/tools/site-setup.php
 *
 * Idempotent: every step sets a value, so a re-run changes nothing. Rank Math must be
 * installed (`wp plugin install seo-by-rank-math --activate`). Values come from
 * ClickUp 86bcc5579: name, address 4791 Woodmere Blvd, phone (334) 801-9952 "for the
 * moment" (Nicolas, 2026-10-12). No ratings or opening hours: nothing verified exists.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

$name  = 'Heart and Vascular Institute of Alabama';
$media = function ( $key ) {
	$ids = get_posts( array( 'post_type' => 'attachment', 'post_status' => 'inherit', 'meta_key' => '_hvia_media_key',
		'meta_value' => $key, 'posts_per_page' => 1, 'fields' => 'ids' ) );
	if ( ! $ids ) { WP_CLI::error( "media key not found: $key (run upload-media.php first)" ); }
	return (int) $ids[0];
};
$home = get_page_by_path( 'home', OBJECT, 'page' );
if ( ! $home ) { WP_CLI::error( 'page `home` not found (run build-all.sh --import first)' ); }

/* ---- Identity ------------------------------------------------------------------ */
update_option( 'blogname', $name );
update_option( 'blogdescription', 'Board-certified vascular and endovascular surgeons in Montgomery, Alabama' );
update_option( 'site_icon', $media( 'hvia-site-icon' ) );
update_option( 'show_on_front', 'page' );
update_option( 'page_on_front', $home->ID );

/* ---- Permalinks: /%postname%/ instead of ?p= ------------------------------------- */
update_option( 'permalink_structure', '/%postname%/' );
flush_rewrite_rules( false );

/* ---- Rank Math ------------------------------------------------------------------- */
if ( ! defined( 'RANK_MATH_VERSION' ) ) { WP_CLI::error( 'Rank Math is not active' ); }

$modules = (array) get_option( 'rank_math_modules', array() );
foreach ( array( 'local-seo', 'rich-snippet', 'sitemap' ) as $m ) {
	if ( ! in_array( $m, $modules, true ) ) { $modules[] = $m; }
}
update_option( 'rank_math_modules', array_values( $modules ) );
update_option( 'rank_math_wizard_completed', true );   // no setup-wizard redirect in wp-admin
// Same as "Skip" on the wizard's account step. Without it (and no connected account)
// Rank Math prints nothing on the front end: no meta, no Open Graph, no schema.
update_option( 'rank_math_registration_skip', 1 );

$logo_id = $media( 'hvia-mark' );
$titles  = (array) get_option( 'rank-math-options-titles', array() );
$titles  = array_merge( $titles, array(
	'knowledgegraph_type'    => 'company',
	'knowledgegraph_name'    => $name,
	'website_name'           => $name,
	'website_alternate_name' => 'HVIA',
	'local_business_type'    => 'MedicalClinic',
	'local_address'          => array(
		'streetAddress'   => '4791 Woodmere Blvd',
		'addressLocality' => 'Montgomery',
		'addressRegion'   => 'AL',
		'postalCode'      => '36106',
		'addressCountry'  => 'US',
	),
	'phone'                  => '+1-334-801-9952',
	'knowledgegraph_logo'    => wp_get_attachment_url( $logo_id ),
	'knowledgegraph_logo_id' => $logo_id,
	'open_graph_image'       => wp_get_attachment_url( $media( 'hvia-new-building' ) ),
	'open_graph_image_id'    => $media( 'hvia-new-building' ),
	// Pages are not articles: no Article schema on them by default.
	'pt_page_default_rich_snippet' => 'off',
) );
update_option( 'rank-math-options-titles', $titles );

/* Home page meta. The prototype title is 75 characters; this one keeps the full name
   and the city under 60. Description: the prototype's, verbatim. */
update_post_meta( $home->ID, 'rank_math_title', 'Heart and Vascular Institute of Alabama | Montgomery, AL' );
update_post_meta( $home->ID, 'rank_math_description',
	'Heart and Vascular Institute of Alabama (HVIA): board-certified vascular and endovascular surgeons in Montgomery, Alabama.' );
update_post_meta( $home->ID, 'rank_math_facebook_image', wp_get_attachment_url( $media( 'hvia-new-building' ) ) );
update_post_meta( $home->ID, 'rank_math_facebook_image_id', $media( 'hvia-new-building' ) );
update_post_meta( $home->ID, 'rank_math_rich_snippet', 'off' );

/* ---- Alt text in the media library (Open Graph and anyone reusing the images) --- */
$alts = array(
	'hvia-new-building'      => 'Rendering of the new HVIA building at 4791 Woodmere Blvd, Montgomery',
	'hvia-team-surgeons'     => 'HVIA surgeons: Dr. Richard Tan, Dr. Ralph Redd and Dr. Irwin White-Gittens',
	'dr-ralph-redd'          => 'Dr. Ralph Redd, MD',
	'dr-richard-tan'         => 'Dr. Richard Tan, MD',
	'dr-irwin-white-gittens' => 'Dr. Irwin White-Gittens, MD',
	'hvia-mark'              => 'Heart and Vascular Institute of Alabama logo',
	'hvia-mark-light'        => 'Heart and Vascular Institute of Alabama logo',
	'hvia-site-icon'         => 'Heart and Vascular Institute of Alabama logo',
);
foreach ( $alts as $key => $alt ) {
	update_post_meta( $media( $key ), '_wp_attachment_image_alt', $alt );
}

/* ---- WordPress sample content (to trash, restorable) --------------------------- */
foreach ( array( 'hello-world' => 'post', 'sample-page' => 'page' ) as $slug => $type ) {
	$p = get_page_by_path( $slug, OBJECT, $type );
	if ( $p && 'trash' !== $p->post_status ) { wp_trash_post( $p->ID ); WP_CLI::log( "trashed $type #{$p->ID} ($slug)" ); }
}
foreach ( get_posts( array( 'post_type' => 'page', 'post_status' => 'draft', 'title' => 'Elementor #8', 'posts_per_page' => -1 ) ) as $p ) {
	wp_trash_post( $p->ID ); WP_CLI::log( "trashed page #{$p->ID} (empty Elementor draft)" );
}

WP_CLI::success( 'site setup done (home #' . $home->ID . ')' );
