#/usr/bin/env bash
run="python funnel_calc.py"
# -s -t month web_users_uk registration_web move_to_zvooq_plus payture_gate_shown payture_gate_purchase_clicked subscription # ZA-418.2 general funnel 
$run -s -t month payture_gate_shown subscription # ZA-418.2 part of general
$run -s bud_page_shown_uc bud_link_clicked_uc app_opened_ip bud_subscriber_via_promocode #ZA-572 bud funnel
$run beeline_subscription_initiated beeline_subscription_successful install_from_beeline #ZA-545 beeline funnel
