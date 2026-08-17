<?php
/**
 * Dolan Design HVAC — accessibility audit fixes.
 *
 * Paste everything below this header into wp-content/themes/Divi-child/functions.php,
 * or drop the whole file into wp-content/mu-plugins/.
 * Needs Divi-child/page.php too — that supplies <main> on Divi-templated pages.
 *
 *   1. <main> landmark    3. image alt text
 *   2. button contrast    4. focus ring
 *
 * Full rationale and measurements: theme-fixes/HANDOFF-notes.md
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Dolan Design HVAC — accessibility fixes for the client audit.
 *
 * 1. <main> landmark. Divi's template only emits <div id="main-content">.
 *    Divi-child/page.php supplies the real <main> on Divi pages; the_content filter
 *    below covers Elementor Full Width pages. Both are needed — keep page.php.
 *
 * 2. Button contrast. The 3 orange "Request Service" buttons on Home were 3.26:1
 *    (AA needs 4.5:1); now #C24A16 = 4.90:1. Theme Builder header buttons excluded.
 *
 * 3. Image alt text. Divi outputs alt="" for inserted images and never reads the
 *    Media Library. Alt is filled in at render — Media Library first, filename as
 *    fallback. To fix any image, set its Alternative Text in Media > Library.
 *
 * 4. Focus ring. Formidable Forms sets outline:none on form fields; restored here.
 *
 * Nothing is written to the database and no page content is edited; everything is
 * applied on output. Full detail: projects/dolan/theme-fixes/HANDOFF-notes.md
 */

/* --- 1. <main> on Elementor Full Width pages ------------------------------
 * Those pages bypass page.php and emit no <main>. Wrapping the content string
 * avoids hunting for a matching close tag in the output buffer. */

add_filter(
	'the_content',
	function ( $content ) {
		if ( ! is_singular() || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		if ( 'elementor_header_footer' !== get_page_template_slug() ) {
			return $content;
		}
		if ( false !== stripos( $content, '<main' ) ) {
			return $content;
		}

		return '<main id="main-content">' . $content . '</main>';
	},
	20
);

/* --- 1 (fallback) + 3. rewrite the page HTML ----------------------------- */

add_action(
	'template_redirect',
	function () {
		if ( is_admin() || is_feed() || wp_doing_ajax() ) {
			return;
		}
		if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
			return;
		}
		// Divi Visual Builder / Elementor editor.
		if ( isset( $_GET['et_fb'] ) || isset( $_GET['elementor-preview'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Recommended
			return;
		}
		ob_start( 'dolan_a11y_html' );
	},
	1
);

/**
 * Output buffer callback.
 *
 * @param string $html Full page HTML.
 * @return string
 */
if ( ! function_exists( 'dolan_a11y_html' ) ) :
function dolan_a11y_html( $html ) {
	if ( false === stripos( $html, '</body>' ) ) {
		return $html;
	}

	// Landmark safety net for templates page.php does not cover (posts, 404).
	// Skipped wherever a <main> already exists.
	if ( ! preg_match( '/<main[\s>]/i', $html ) && ! preg_match( '/\srole=(["\'])main\1/i', $html ) ) {
		$targets = array(
			'/<div(\s[^>]*?)?\sid=(["\'])main-content\2/i'               => '<div$1 role="main" id=$2main-content$2',
			'/<div([^>]*\sdata-elementor-type=(["\'])wp-page\2[^>]*)>/i' => '<div role="main"$1>',
		);

		foreach ( $targets as $pattern => $replacement ) {
			$count  = 0;
			$result = preg_replace( $pattern, $replacement, $html, 1, $count );
			if ( $count && null !== $result ) {
				$html = $result;
				break;
			}
		}
	}

	// null on a PCRE backtrack limit would blank the page, hence the guard.
	$result = preg_replace_callback( '/<img\b[^>]*>/i', 'dolan_a11y_img', $html );

	return ( null === $result ) ? $html : $result;
}
endif;

/**
 * Give a single <img> an alt attribute if it has none.
 *
 * Divi renders alt="" for every inserted image, so empty counts as missing here.
 *
 * @param array $m preg matches.
 * @return string
 */
if ( ! function_exists( 'dolan_a11y_img' ) ) :
function dolan_a11y_img( $m ) {
	$tag = $m[0];

	// Explicitly decorative — leave alone.
	if ( preg_match( '/\srole=(["\'])presentation\1/i', $tag )
		|| preg_match( '/\saria-hidden=(["\'])true\1/i', $tag ) ) {
		return $tag;
	}

	$has_alt = preg_match( '/\salt=(["\'])(.*?)\1/is', $tag, $alt_match );
	if ( $has_alt && '' !== trim( $alt_match[2] ) ) {
		return $tag;
	}

	// Prefer a lazy-loader's real URL over a base64 placeholder.
	$src_url = '';
	foreach ( array( 'data-src', 'data-lazy-src', 'src' ) as $attr ) {
		$pattern = '/\s' . preg_quote( $attr, '/' ) . '=(["\'])(.*?)\1/i';
		if ( preg_match( $pattern, $tag, $found ) && 0 !== stripos( trim( $found[2] ), 'data:' ) ) {
			$src_url = $found[2];
			break;
		}
	}

	if ( '' === $src_url ) {
		return $tag;
	}

	// Media Library wins, so editors can fix any image without touching code.
	$alt = dolan_a11y_alt_from_library( $src_url );
	if ( '' === $alt ) {
		$alt = dolan_a11y_alt_from_src( $src_url );
	}
	if ( '' === $alt ) {
		return $tag;
	}

	$attr = 'alt="' . esc_attr( $alt ) . '"';

	// Not preg_replace — alt text can contain $ and \, read as backreferences.
	return $has_alt
		? str_replace( $alt_match[0], ' ' . $attr, $tag )
		: substr_replace( $tag, '<img ' . $attr, 0, 4 );
}
endif;

/**
 * Alt text from the Media Library. Divi never reads it for inserted images.
 *
 * @param string $url Image src.
 * @return string
 */
if ( ! function_exists( 'dolan_a11y_alt_from_library' ) ) :
function dolan_a11y_alt_from_library( $url ) {
	$index = dolan_a11y_alt_index();
	$stem  = dolan_a11y_stem( $url );

	return ( '' !== $stem && isset( $index[ $stem ] ) ) ? $index[ $stem ] : '';
}
endif;

/**
 * Reduce a filename to a stem that survives WordPress and CompressX rewriting.
 *
 * attachment_url_to_postid() is no use here: CompressX republishes into a different
 * month folder with a new extension and a hash, so the URL shares no path with the
 * attachment. 2025/05/servicing_a_mini_split-scaled.png is served as
 * 2026/01/servicing_a_mini_split-400x284_e7ad1d3340.webp — both stem to the same thing.
 *
 * @param string $path Filename, path or URL.
 * @return string
 */
if ( ! function_exists( 'dolan_a11y_stem' ) ) :
function dolan_a11y_stem( $path ) {
	$name = basename( strtok( (string) $path, '?' ) );

	// Stacked extensions: CompressX writes photo.jpg.webp.
	while ( preg_match( '/\.(jpe?g|png|webp|gif|svg|avif)$/i', $name ) ) {
		$name = (string) preg_replace( '/\.[^.]+$/', '', $name );
	}

	$name = preg_replace( '/-scaled$/i', '', $name );
	$name = preg_replace( '/[_-][0-9a-f]{6,}$/i', '', $name ); // hash
	$name = preg_replace( '/-\d+x\d+$/', '', $name );          // resize
	$name = preg_replace( '/[_-][0-9a-f]{6,}$/i', '', $name );

	return strtolower( trim( (string) $name ) );
}
endif;

/**
 * stem => alt index for every attachment that has Alternative Text.
 * One query, cached for a day, instead of a lookup per image.
 *
 * @return array<string,string>
 */
if ( ! function_exists( 'dolan_a11y_alt_index' ) ) :
function dolan_a11y_alt_index() {
	static $index = null;

	if ( null !== $index ) {
		return $index;
	}

	$cached = get_transient( 'dolan_alt_index' );
	if ( is_array( $cached ) ) {
		$index = $cached;
		return $index;
	}

	global $wpdb;

	$rows = $wpdb->get_results( // phpcs:ignore WordPress.DB.DirectDatabaseQuery
		"SELECT f.meta_value AS file, a.meta_value AS alt
		   FROM {$wpdb->postmeta} a
		   INNER JOIN {$wpdb->postmeta} f
		           ON f.post_id = a.post_id AND f.meta_key = '_wp_attached_file'
		  WHERE a.meta_key = '_wp_attachment_image_alt'
		    AND a.meta_value <> ''"
	);

	$index = array();
	foreach ( (array) $rows as $row ) {
		$stem = dolan_a11y_stem( $row->file );
		if ( '' !== $stem && ! isset( $index[ $stem ] ) ) {
			$index[ $stem ] = $row->alt;
		}
	}

	set_transient( 'dolan_alt_index', $index, DAY_IN_SECONDS );

	return $index;
}
endif;

/**
 * Drop the cached index when an attachment's alt text is edited.
 *
 * @param int    $meta_id  Meta row id.
 * @param int    $post_id  Attachment id.
 * @param string $meta_key Meta key.
 * @return void
 */
if ( ! function_exists( 'dolan_a11y_flush_alt_cache' ) ) :
function dolan_a11y_flush_alt_cache( $meta_id, $post_id, $meta_key ) {
	if ( '_wp_attachment_image_alt' === $meta_key ) {
		delete_transient( 'dolan_alt_index' );
	}
}
endif;

add_action( 'updated_post_meta', 'dolan_a11y_flush_alt_cache', 10, 3 );
add_action( 'added_post_meta', 'dolan_a11y_flush_alt_cache', 10, 3 );

/**
 * Last resort: build alt text from the filename.
 *
 * $overrides covers filenames that are codes rather than words. Add a line there
 * when a new image would otherwise read as nonsense — or better, give it
 * Alternative Text in the Media Library and this function never runs for it.
 *
 * @param string $url Image src.
 * @return string
 */
if ( ! function_exists( 'dolan_a11y_alt_from_src' ) ) :
function dolan_a11y_alt_from_src( $url ) {
	$overrides = array(
		'gdmnlogo'               => 'Goodman Air Conditioning and Heating logo',
		'air-conditioner-2'      => 'Wall-mounted mini-split air handler',
		'better_air_better_life' => 'Better Air Better Life 2025 free HVAC system giveaway',
		'DolanHVAC_RSMQuad'      => '$99 fall maintenance special',

		// Home page service gallery — the images the client asked to have described.
		'Group-Photo_updated' => 'The Dolan Design Heating and Cooling team outside the company shop with two branded service vans',
		'image4-3'            => 'A Dolan Design service van parked outside a coastal home on a service call',
		'image00'             => 'Three outdoor air conditioner condensing units installed on a raised platform beside a home',
		'IMG_0476'            => 'A newly installed Mitsubishi Electric mini split outdoor unit on a concrete pad beside a brick home',
		'519141176'           => 'A crane lifting HVAC equipment to the roof of a multi-story building',
		'518704760'           => 'A crane lowering a crated HVAC unit to a technician waiting on the rooftop',
	);

	$path = wp_parse_url( $url, PHP_URL_PATH );
	if ( ! $path ) {
		return '';
	}
	$name = basename( $path );

	foreach ( $overrides as $needle => $text ) {
		if ( false !== stripos( $name, $needle ) ) {
			return $text;
		}
	}

	// Stacked extensions: CompressX writes photo.jpg.webp.
	while ( preg_match( '/\.(jpe?g|png|webp|gif|svg|avif)$/i', $name ) ) {
		$name = (string) preg_replace( '/\.[^.]+$/', '', $name );
	}

	$name = preg_replace( '/\.svg_?$/i', '', $name );          // Rheem_logo.svg_
	$name = preg_replace( '/-scaled$/i', '', $name );
	$name = preg_replace( '/[_-]\d+x\d+/', ' ', $name );       // resize
	$name = preg_replace( '/[_-][0-9a-f]{6,}$/i', '', $name ); // hash
	$name = preg_replace( '/[\s_-]+/', ' ', $name );
	$name = trim( preg_replace( '/\s*\d+$/', '', $name ) );    // trailing counter

	// Meaningless tokens, so camera dumps fall through to the generic rather than
	// shipping alt="IMG". "before"/"after" are deliberately absent — before/after
	// installation shots are a standard HVAC content type.
	$junk = array(
		'img', 'image', 'pic', 'photo', 'dsc', 'dscn', 'screenshot', 'untitled',
		'copy', 'final', 'edited', 'rotated', 'scaled', 'proof', 'n',
	);

	$words = array_filter(
		explode( ' ', $name ),
		function ( $w ) use ( $junk ) {
			if ( '' === $w || ctype_digit( $w ) ) {
				return false;
			}
			// Hash fragment: hex only, and contains a digit so real words like
			// "facade" and "decade" are not caught.
			if ( strlen( $w ) >= 4 && preg_match( '/^[0-9a-f]+$/i', $w ) && preg_match( '/\d/', $w ) ) {
				return false;
			}
			return ! in_array( strtolower( preg_replace( '/\d+/', '', $w ) ), $junk, true );
		}
	);

	$name = trim( implode( ' ', $words ) );

	if ( strlen( $name ) < 3 ) {
		return 'Dolan Design HVAC';
	}

	return ucfirst( $name );
}
endif;

/* --- 2 + 4. stylesheet ---------------------------------------------------- */

add_action(
	'wp_enqueue_scripts',
	function () {
		$css = '
/* 2. The 3 orange "Request Service" buttons on Home were 3.26:1; #C24A16 is 4.90:1.
   :not(_tb_) keeps the 8 Theme Builder header buttons out of it. Hover and focus are
   stated so the base !important does not carry into them by accident. */
body.page-id-230601 .et_pb_button:not([class*="_tb_"]),
body.page-id-230601 .et_pb_button:not([class*="_tb_"]):hover,
body.page-id-230601 .et_pb_button:not([class*="_tb_"]):focus,
body.page-id-230601 .et_pb_promo_button:not([class*="_tb_"]),
body.page-id-230601 .et_pb_promo_button:not([class*="_tb_"]):hover,
body.page-id-230601 .et_pb_promo_button:not([class*="_tb_"]):focus {
	background-color: #C24A16 !important;
	border-color: #C24A16 !important;
	color: #FFFFFF !important;
}

/* 4. Formidable Forms sets outline:none on form fields. Dark outline plus a white halo
   so it reads on white, on #EDF4FF bands, and on #0C4096 heroes alike. */
a:focus-visible,
button:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
summary:focus-visible,
[tabindex]:focus-visible,
.et_pb_button:focus-visible,
.et_pb_promo_button:focus-visible,
.elementor-button:focus-visible,
.with_frm_style input:focus-visible,
.with_frm_style select:focus-visible,
.with_frm_style textarea:focus-visible,
.with_frm_style button:focus-visible {
	outline: 3px solid #0C4096 !important;
	outline-offset: 2px !important;
	box-shadow: 0 0 0 6px rgba(255, 255, 255, 0.95) !important;
}';

		wp_register_style( 'dolan-a11y', false, array(), '1.0.0' );
		wp_enqueue_style( 'dolan-a11y' );
		wp_add_inline_style( 'dolan-a11y', $css );
	},
	99
);
