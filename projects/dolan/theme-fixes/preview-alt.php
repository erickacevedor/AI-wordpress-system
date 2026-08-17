<?php
/**
 * Dev tool — NOT deployed. Shows what alt text the filename rule produces.
 *
 *   php preview-alt.php            # the 9 images the audit flagged
 *   php preview-alt.php --all      # every image in the Flywheel backup
 *
 * Run this after adding an $overrides entry to confirm the result reads well.
 */

define( 'ABSPATH', __DIR__ );
function add_action( ...$a ) {}
function esc_attr( $s ) { return htmlspecialchars( $s, ENT_QUOTES, 'UTF-8' ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }

require __DIR__ . '/dolan-a11y-fixes.php';

$base = 'https://dolandesignhvac.com/wp-content/uploads/2026/01/';

$flagged = array(
	'Honeywell_logo_a7990cd700.webp',
	'trane-logo_94259ac5b2.webp',
	'gdmnlogo_8f8552e372.webp',
	'mitsubishi-logo_5b5a0a3859.webp',
	'aprilaire2.png',
	'Rheem_logo.svg_.png',
	'air-conditioner-2_d60ce77315.webp',
	'better_air_better_life_2025_contest_ad_2.png',
	'DolanHVAC_RSMQuad_WLS1025_PROOF-scaled.png',
);

/**
 * Flag alt text that reads like a filename rather than a description.
 *
 * @param string $alt Generated alt.
 * @return bool
 */
function looks_wrong( $alt ) {
	// Years read fine in alt text; anything else numeric is a leftover id or hash.
	$stripped = preg_replace( '/\b(19|20)\d{2}\b/', '', $alt );

	return 'Dolan Design HVAC' === $alt          // hit the fallback
		|| (bool) preg_match( '/\d{3,}/', $stripped )
		|| strlen( $alt ) < 4;
}

echo "=== the 9 images the audit flagged ===\n";
printf( "%-46s %s\n", 'FILE', 'GENERATED ALT' );
foreach ( $flagged as $f ) {
	$alt = dolan_a11y_alt_from_src( $base . $f );
	printf( "%-46s %s%s\n", $f, $alt, looks_wrong( $alt ) ? '   <-- REVIEW' : '' );
}

if ( ! in_array( '--all', $argv, true ) ) {
	echo "\nRun with --all to scan every image in the backup.\n";
	exit( 0 );
}

$uploads = 'D:/Desktop/Desktop/DolanDesignHVAC-080426-backup/files/wp-content/uploads';
if ( ! is_dir( $uploads ) ) {
	echo "\nBackup not found at $uploads\n";
	exit( 1 );
}

$it    = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $uploads ) );
$seen  = array();
$flags = array();
$total = 0;

foreach ( $it as $file ) {
	if ( ! $file->isFile() ) {
		continue;
	}
	if ( ! preg_match( '/\.(jpe?g|png|webp|gif|svg)$/i', $file->getFilename() ) ) {
		continue;
	}
	// Skip WordPress's generated resize variants.
	if ( preg_match( '/-\d+x\d+\.[a-z]+$/i', $file->getFilename() ) ) {
		continue;
	}
	$name = $file->getFilename();
	if ( isset( $seen[ $name ] ) ) {
		continue;
	}
	$seen[ $name ] = true;
	$total++;

	$alt = dolan_a11y_alt_from_src( $base . $name );
	if ( looks_wrong( $alt ) ) {
		$flags[ $name ] = $alt;
	}
}

echo "\n=== scanned $total unique originals ===\n";
if ( ! $flags ) {
	echo "No filenames produced suspicious alt text.\n";
	exit( 0 );
}

echo count( $flags ) . " would produce alt worth reviewing:\n";
printf( "%-54s %s\n", 'FILE', 'GENERATED ALT' );
foreach ( $flags as $f => $alt ) {
	printf( "%-54s %s\n", substr( $f, 0, 54 ), $alt );
}
