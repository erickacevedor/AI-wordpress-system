<?php
/**
 * Create (or rebuild) the WordPress menu the header's Nav Menu widget shows.
 *
 * Run:  wp eval-file projects/newman-air/tools/make-menus.php
 *
 * "Newman Main" (slug newman-main), same items as the V2.1 header (Manuel's sitetree):
 *   Services (CSS class nw-mega: shown as the mega menu)
 *     4 groups (class mega-group + an icon class), each with its service pages,
 *     then a CTA item (class mega-cta)
 *   Service Areas (6 cities), Maintenance Plan, Financing, Blog, About Us, Contact Us.
 * Group headings link to "#" and are not clickable on desktop (CSS). Edit the menu
 * afterwards in Appearance > Menus; re-running this script rebuilds it from scratch.
 */

if ( ! defined( 'ABSPATH' ) ) { exit( 1 ); }

$slug = 'newman-main';
$menu = wp_get_nav_menu_object( $slug );
if ( $menu ) {
	foreach ( wp_get_nav_menu_items( $menu->term_id, array( 'post_status' => 'any' ) ) as $item ) {
		wp_delete_post( $item->ID, true );
	}
	$menu_id = $menu->term_id;
} else {
	$menu_id = wp_create_nav_menu( 'Newman Main' );
	wp_update_term( $menu_id, 'nav_menu', array( 'slug' => $slug ) );
}

/** Add one item; pages are linked as pages (so a slug change follows), the rest as custom links. */
function newman_menu_item( $menu_id, $title, $url, $parent = 0, $classes = '' ) {
	$args = array(
		'menu-item-title'     => $title,
		'menu-item-status'    => 'publish',
		'menu-item-parent-id' => $parent,
		'menu-item-classes'   => $classes,
	);
	$path = trim( (string) wp_parse_url( $url, PHP_URL_PATH ), '/' );
	$page = ( $path && '#' !== $url ) ? get_page_by_path( $path, OBJECT, 'page' ) : null;
	if ( $page ) {
		$args['menu-item-object-id'] = $page->ID;
		$args['menu-item-object']    = 'page';
		$args['menu-item-type']      = 'post_type';
	} else {
		$args['menu-item-url']  = $url;
		$args['menu-item-type'] = 'custom';
	}
	return wp_update_nav_menu_item( $menu_id, 0, $args );
}

$groups = array(
	array( 'Air Conditioning', 'ic-snow', array(
		array( 'AC Installation', '/services/ac-installation/' ),
		array( 'AC Repair', '/services/ac-repair/' ),
		array( 'AC Maintenance', '/services/maintenance/' ),
	) ),
	array( 'Heating', 'ic-flame', array(
		array( 'Heating Installation', '/services/heating-installation/' ),
		array( 'Heating Repair', '/services/heating-repair/' ),
		array( 'Heating Maintenance', '/services/maintenance/' ),
	) ),
	array( 'Indoor Air Quality', 'ic-air', array(
		array( 'Air Cleaners', '/services/air-cleaners/' ),
		array( 'Air Handlers', '/services/air-handlers/' ),
		array( 'Germicidal Lights', '/services/germicidal-lights/' ),
	) ),
	array( 'Additional Services', 'ic-plus', array(
		array( 'Heat Pumps', '/services/heat-pumps/' ),
		array( 'Ductless Mini Splits', '/services/ductless/' ),
		array( 'Ductwork', '/services/ductwork/' ),
		array( 'Thermostats', '/services/thermostats/' ),
		array( 'Commercial HVAC', '/services/commercial/' ),
	) ),
);

$services = newman_menu_item( $menu_id, 'Services', '/services/', 0, 'nw-mega' );
foreach ( $groups as $g ) {
	$gid = newman_menu_item( $menu_id, $g[0], '#', $services, 'mega-group ' . $g[1] );
	foreach ( $g[2] as $it ) {
		newman_menu_item( $menu_id, $it[0], $it[1], $gid );
	}
}
newman_menu_item( $menu_id, '<strong>Not sure what you need?</strong> Upfront $75 diagnostic. Call (423) 753-7788',
	'/contact-us/', $services, 'mega-cta' );

$areas = newman_menu_item( $menu_id, 'Service Areas', '/service-area/', 0, 'nw-drop' );
foreach ( array( 'Bristol', 'Elizabethton', 'Gray', 'Greeneville', 'Jonesborough', 'Kingsport' ) as $city ) {
	newman_menu_item( $menu_id, $city, '/service-area/' . sanitize_title( $city ) . '/', $areas );
}
foreach ( array( array( 'Maintenance Plan', '/maintenance-plan/' ), array( 'Financing', '/financing/' ),
	array( 'Blog', '/blog/' ), array( 'About Us', '/about-us/' ), array( 'Contact Us', '/contact-us/' ) ) as $it ) {
	newman_menu_item( $menu_id, $it[0], $it[1] );
}

WP_CLI::log( sprintf( 'menu #%d (%s): %d items', $menu_id, $slug, count( wp_get_nav_menu_items( $menu_id ) ) ) );
