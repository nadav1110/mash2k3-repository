<?php
/*
Plugin Name: eSIM Usage Tracker
Description: מציג כרטיסי שימוש דינמיים לכל חבילות ה-eSIM
Version: 2.2
*/

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

function esim_usage_tracker_shortcode() {
    if (!is_user_logged_in()) {
        return '<div class="esim-notice">אנא התחבר כדי לצפות בנתוני השימוש.</div>';
    }

    global $wpdb;
    $current_user = wp_get_current_user();
  
    // Get all active eSIMs
    $esims = $wpdb->get_results($wpdb->prepare(
        "SELECT 
            items.data_amount,
            items.validity_period,
            logs.created_date,
            status.remaining_quantity,
            status.initial_quantity,
            items.iccid,
            items.country
         FROM {$wpdb->prefix}esimgo_bundle_purchase_items items
         INNER JOIN {$wpdb->prefix}esimgo_bundle_purchase_logs logs 
            ON items.order_id = logs.order_id
         LEFT JOIN {$wpdb->prefix}esimgo_bundle_status status 
            ON items.iccid = status.iccid
         WHERE items.user_id = %d
         AND logs.status = 'completed'
         ORDER BY logs.created_date DESC",
        $current_user->ID
    ));

    // Load country mapping file
    $json_file_path = WP_CONTENT_DIR . '/plugins/gbams123-esim-go-integration/includes/countries_in_hebrew.json';
    $country_map = file_exists($json_file_path) ? json_decode(file_get_contents($json_file_path), true) : [];

    // Prepare data container
    $all_esim_data = [];
	
    foreach ($esims as $esim) {
		// Map country name from JSON file
        $original_country = strtolower(trim($esim->country));
        $mapped_name = $country_map[$original_country] ?? $esim->country;
        $country_slug = sanitize_title($mapped_name);

        // Get product URL for this specific country
        $product_url = '';
        if (!empty($country_slug)) {
            $product = get_page_by_path($country_slug, OBJECT, 'product');
            if ($product) {
                $product_url = get_permalink($product->ID) . '?topup=true&esim=' . $esim->iccid;
            }
        }
        
        // Fallback URL if product not found
        if (empty($product_url)) {
            $product_url = 'https://www.nisim-esim.co.il/all-destinations/?topup=true&esim=' . $esim->iccid;
        }

        // Data calculations (convert GB to MB if needed)
        $total_data = $esim->initial_quantity ?: ($esim->data_amount * 1000);
        $remaining_data = max(0, $esim->remaining_quantity ?: 0);
        $used_data = $total_data - $remaining_data;
        
        // Validity calculations
        $expiry_time = strtotime($esim->created_date) + ($esim->validity_period * DAY_IN_SECONDS);
        $current_time = time();
        $days_remaining = max(0, floor(($expiry_time - $current_time) / DAY_IN_SECONDS));
        $days_used = $esim->validity_period - $days_remaining;
        
        $all_esim_data[] = [
            'data' => [
                'used' => $used_data,
                'total' => $total_data,
                'remaining' => $remaining_data,
                'percent' => $total_data > 0 ? min(100, ($used_data / $total_data) * 100) : 0,
                'iccid' => $esim->iccid,
                'country' => $mapped_name,
                'product_url' => $product_url
            ],
            'validity' => [
                'used' => $days_used,
                'total' => $esim->validity_period,
                'remaining' => $days_remaining,
                'percent' => $days_remaining <= 0 ? 100 : min(100, ($days_used / $esim->validity_period) * 100)
            ]
        ];
    }

    ob_start(); ?>

    <div class="esim-usage-tracker">
        <style>
            .esim-usage-tracker {
                font-family: "IBM", Sans-serif!important;
                width: 100%;
            }
            .cards-container {
                display: flex;
                gap: 30px;
                width: 100%;
                margin: 0 auto;
                flex-wrap: wrap;
            }
            .card {
                background-image: url('https://www.nisim-esim.co.il/wp-content/uploads/2024/09/back.jpg');
                background-size: cover;
                border: 1px solid #63b2e173;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
                padding: 24px;
                width: 48%!important;
            }
            .card-header {
                font-size: 18px;
                font-weight: 600;
                color: #00325E;
                margin-bottom: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .section {
                display: flex;
                flex-direction: column;
            }
            .section-title {
                font-size: 16px;
                font-weight: 500;
                color: #00325E;
                margin-bottom: 8px;
            }
            .data-value,
            .days-value {
                display: flex;
                align-items: baseline;
                flex-wrap: wrap;
                gap: 8px;
            }
            .blance-data,
            .left-days {
                font-size: 30px;
                font-weight: 700;
                color: #00325E;
                margin: 12px 0;
            }
            .total-data,
            .total-days {
                font-size: 18px;
                font-weight: 500;
                color: #818181;
                margin: 12px 0;
            }
            .progress-container {
                height: 15px;
                background-color: #f5f5f7;
                border-radius: 7.5px;
                margin: 20px 0;
                overflow: hidden;
                position: relative;
            }
            .progress-bar {
                height: 100%;
                border-radius: 7.5px;
                background-color: #00325E;
                position: absolute;
                top: 0;
                left: 0;
                transition: width 0.8s ease-out;
                width: 0;
            }
            .top-up-btn {
                color: white;
                font-size: 18px;
                line-height: 18px;
                font-weight: 400;
                background-color: #00325E;
                border: none;
                border-radius: 32px;
                padding: 14px 28px;
                cursor: pointer;
                transition: transform 0.2s ease;
                width: 100%;
                text-align: center;
                display: block;
                text-decoration: none;
            }
            .top-up-btn:hover {
                color: #fff;
                background-color: #63B2E2;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .esim-notice {
                text-align: center;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                color: #6c757d;
            }
            .icc-id {
                font-size: 14px;
                color: #666;
                word-break: break-all;
            }
				
            @media (max-width: 1300px) {
                .card {
                    width: 100%!important;
                    max-width: 100%!important;
                }
            }
        </style>

        <div class="cards-container">
            <?php foreach ($all_esim_data as $esim): ?>
            <div class="card">
                <div class="card-header">
                    <span><?php echo esc_html($esim['data']['country']); ?> eSIM</span>
                    <span class="icc-id"><?php echo esc_html($esim['data']['iccid']); ?></span>
                </div>
                
                <!-- Data Card -->
                <div class="section">
                    <div class="section-title">דאטה</div>
                    <div class="data-value">
                        <span class="blance-data" data-remaining="<?php echo $esim['data']['remaining']; ?>">0 GB</span>
                        <span class="total-data" data-total="<?php echo $esim['data']['total']; ?>">מתוך 0 GB</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" data-percent="<?php echo $esim['data']['percent']; ?>"></div>
                    </div>
                </div>
                
                <!-- Validity Card -->
                <div class="section">
                    <div class="section-title">תוקף</div>
                    <div class="days-value">
                        <span class="left-days" data-remaining="<?php echo $esim['validity']['remaining']; ?>">0 ימים</span>
                        <span class="total-days" data-total="<?php echo $esim['validity']['total']; ?>">מתוך 0 ימים</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" data-percent="<?php echo $esim['validity']['percent']; ?>"></div>
                    </div>
                </div>
                
                <a href="<?php echo esc_url($esim['data']['product_url']); ?>" class="top-up-btn">הוסף דאטה</a>
            </div>
            <?php endforeach; ?>
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Format data for display
                function formatData(value, isTotal = false) {
                    if (isTotal) {
                        // Total data is always displayed as an integer in GB
                        return Math.floor(value / 1000) + ' GB';
                    }
                    // Remaining or used data
                    if (value >= 1000) {
                        // Display in GB with one decimal place for values >= 1GB
                        return (value / 1000).toFixed(1) + ' GB';
                    }
                    // Display in MB for values < 1GB
                    return value + ' MB';
                }
                
                // Process all cards
                document.querySelectorAll('.card').forEach(card => {
                    // Update Data Card
                    const dataRemaining = card.querySelector('[data-remaining]').getAttribute('data-remaining');
                    const dataTotal = card.querySelector('[data-total]').getAttribute('data-total');
                    const dataPercent = card.querySelector('.progress-bar').getAttribute('data-percent');
                    
                    card.querySelector('.blance-data').textContent = formatData(dataRemaining);
                    card.querySelector('.total-data').textContent = 'מתוך ' + formatData(dataTotal, true);
                    
                    // Update Validity Card
                    const daysRemaining = card.querySelectorAll('[data-remaining]')[1].getAttribute('data-remaining');
                    const daysTotal = card.querySelectorAll('[data-total]')[1].getAttribute('data-total');
                    const validityPercent = card.querySelectorAll('.progress-bar')[1].getAttribute('data-percent');
                    
                    card.querySelector('.left-days').textContent = daysRemaining + ' ימים';
                    card.querySelector('.total-days').textContent = 'מתוך ' + daysTotal + ' ימים';
                    
                    // Animate progress bars
                    setTimeout(() => {
                        card.querySelectorAll('.progress-bar').forEach((bar, index) => {
                            const percent = index === 0 ? dataPercent : validityPercent;
                            bar.style.width = percent + '%';
                        });
                    }, 100);
                });
            });
        </script>
    </div>

    <?php
    return ob_get_clean();
}

// Register the shortcode
add_shortcode('esim_usage_tracker', 'esim_usage_tracker_shortcode');

// Add plugin activation hook
register_activation_hook(__FILE__, 'esim_usage_tracker_activate');

function esim_usage_tracker_activate() {
    // Plugin activation code if needed
}

// Add plugin deactivation hook
register_deactivation_hook(__FILE__, 'esim_usage_tracker_deactivate');

function esim_usage_tracker_deactivate() {
    // Plugin deactivation code if needed
}