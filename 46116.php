46116
46111
46102
46095
46066
26479
24161
2251
2115
46797
46436

wp post delete $(wp post list --post_type=post --format=ids | grep -v -E '^(46436|46797|2115|2251|24161|26479|46066|46095|46102|46111|46116)$') --force

add_action('init', function () {
    if (!is_admin()) return;

    $keep_ids = [46436, 46797, 2115, 2251, 24161, 26479, 46066, 46095, 46102, 46111, 46116]; // <-- your real post IDs
    $args = [
        'post_type'      => 'post',
        'post__not_in'   => $keep_ids,
        'posts_per_page' => -1,
        'fields'         => 'ids',
    ];

    $posts = get_posts($args);
    foreach ($posts as $post_id) {
        wp_delete_post($post_id, true); // true = force delete
    }

    exit('Deleted all posts except the originals.');
});
