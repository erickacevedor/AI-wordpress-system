<?php
/**
 * Lenz Brand Marquee — an infinite, seamless, pausable logo strip.
 *
 * WHY A CUSTOM WIDGET
 * Elementor has no marquee. The effect needs two identical tracks scrolling left by
 * exactly one track width, so the moment the first fully exits the second is pixel
 * aligned where it started. The edges are faded with `mask-image`, which Elementor
 * also cannot express. Both live in lenz-core.css; this widget only supplies markup.
 *
 * WHY THE CLONE IS RENDERED SERVER-SIDE
 * The static build cloned the track in JavaScript. Rendering both tracks here means
 * the seam works with JS disabled, and the clone can be marked aria-hidden and taken
 * out of the tab order at render time rather than patched afterwards — so the nine
 * brands are announced once, not twice.
 *
 * @package lenz-core
 */

defined( 'ABSPATH' ) || exit;

class Lenz_Marquee_Widget extends \Elementor\Widget_Base {

	public function get_name() {
		return 'lenz-marquee';
	}

	public function get_title() {
		return esc_html__( 'Lenz Brand Marquee', 'lenz-core' );
	}

	public function get_icon() {
		return 'eicon-post-slider';
	}

	public function get_categories() {
		return array( 'general' );
	}

	public function get_keywords() {
		return array( 'lenz', 'marquee', 'brands', 'logos' );
	}

	protected function register_controls() {
		$this->start_controls_section( 'section_brands', array(
			'label' => esc_html__( 'Brands', 'lenz-core' ),
		) );

		$repeater = new \Elementor\Repeater();

		$repeater->add_control( 'brand_name', array(
			'label'       => esc_html__( 'Name', 'lenz-core' ),
			'type'        => \Elementor\Controls_Manager::TEXT,
			'default'     => '',
			'label_block' => true,
		) );

		/* Optional on purpose: with no image the widget renders an accessible text
		   wordmark, so the strip works before the manufacturer logo files land and
		   upgrades cleanly once they do. */
		$repeater->add_control( 'brand_logo', array(
			'label'       => esc_html__( 'Logo (optional)', 'lenz-core' ),
			'type'        => \Elementor\Controls_Manager::MEDIA,
			'description' => esc_html__( 'Leave empty to render the name as a text wordmark.', 'lenz-core' ),
		) );

		$repeater->add_control( 'brand_url', array(
			'label'   => esc_html__( 'Link', 'lenz-core' ),
			'type'    => \Elementor\Controls_Manager::URL,
			'default' => array( 'url' => '', 'is_external' => true ),
		) );

		$this->add_control( 'brands', array(
			'type'        => \Elementor\Controls_Manager::REPEATER,
			'fields'      => $repeater->get_controls(),
			'title_field' => '{{{ brand_name }}}',
			'default'     => array(),
		) );

		$this->add_control( 'speed', array(
			'label'      => esc_html__( 'Loop duration (seconds)', 'lenz-core' ),
			'type'       => \Elementor\Controls_Manager::SLIDER,
			'size_units' => array( 's' ),
			'range'      => array( 's' => array( 'min' => 10, 'max' => 120 ) ),
			'default'    => array( 'unit' => 's', 'size' => 42 ),
			'selectors'  => array(
				'{{WRAPPER}} .lenz-marquee__track' => 'animation-duration: {{SIZE}}s;',
			),
		) );

		$this->end_controls_section();
	}

	/**
	 * One track. Rendered twice — the second aria-hidden and untabbable.
	 */
	private function render_track( $brands, $is_clone = false ) {
		$classes = 'lenz-marquee__track' . ( $is_clone ? ' lenz-marquee__track--dupe' : '' );
		?>
		<div class="<?php echo esc_attr( $classes ); ?>" <?php echo $is_clone ? 'aria-hidden="true"' : ''; ?>>
			<?php foreach ( $brands as $brand ) :
				$name = isset( $brand['brand_name'] ) ? $brand['brand_name'] : '';
				if ( '' === trim( $name ) ) {
					continue;
				}
				$url  = ! empty( $brand['brand_url']['url'] ) ? $brand['brand_url']['url'] : '';
				$logo = ! empty( $brand['brand_logo']['url'] ) ? $brand['brand_logo']['url'] : '';
				$tag  = $url ? 'a' : 'span';
				?>
				<<?php echo $tag; ?> class="lenz-brand-logo"
					<?php if ( $url ) : ?>
						href="<?php echo esc_url( $url ); ?>" target="_blank" rel="noopener noreferrer"
					<?php endif; ?>
					<?php if ( $is_clone ) : ?>
						tabindex="-1"
					<?php elseif ( $url ) : ?>
						aria-label="<?php echo esc_attr( sprintf(
							/* translators: %s: manufacturer name */
							__( '%s HVAC equipment serviced by Lenz', 'lenz-core' ), $name ) ); ?>"
					<?php endif; ?>
				>
					<?php if ( $logo ) : ?>
						<img src="<?php echo esc_url( $logo ); ?>"
							alt="<?php echo $is_clone ? '' : esc_attr( $name ); ?>"
							loading="lazy" decoding="async" />
					<?php else : ?>
						<span class="lenz-brand-logo__wordmark"><?php echo esc_html( $name ); ?></span>
					<?php endif; ?>
				</<?php echo $tag; ?>>
			<?php endforeach; ?>
		</div>
		<?php
	}

	protected function render() {
		$settings = $this->get_settings_for_display();
		$brands   = isset( $settings['brands'] ) && is_array( $settings['brands'] ) ? $settings['brands'] : array();

		if ( empty( $brands ) ) {
			return;
		}
		?>
		<div class="lenz-marquee" data-marquee>
			<?php
			$this->render_track( $brands, false );
			$this->render_track( $brands, true );
			?>
		</div>
		<?php
	}
}
