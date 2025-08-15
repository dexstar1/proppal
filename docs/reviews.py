from fasthtml.common import *

def Reviews():
    return Section(
        H3('Review'),
        P('Review/comment component that supports child reviews/comments.', cls='text-gray-500'),
        Hr(),
        H5(),
        Div(
            Div(
                Div(
                    'Body',
                    Div(
                        Div(
                            Div(
                                'Avatar',
                                Div(
                                    Span(
                                        I('', cls='fa fa-user'),
                                        cls='avatar-title rounded-circle'
                                    ),
                                    cls='avatar avatar-xxl mb-6 mb-md-0'
                                ),
                                cls='col-12 col-md-4 col-lg-3 col-xl-2'
                            ),
                            Div(
                                'Header',
                                Div(
                                    Div(
                                        'Rating',
                                        Div(
                                            Div(I('', cls='fas fa-star'), cls='rating-item'),
                                            Div(I('', cls='fas fa-star'), cls='rating-item'),
                                            Div(I('', cls='fas fa-star'), cls='rating-item'),
                                            Div(I('', cls='fas fa-star'), cls='rating-item'),
                                            Div(I('', cls='fas fa-star'), cls='rating-item'),
                                            cls='rating fs-sm text-dark'
                                        ),
                                        cls='col-12'
                                    ),
                                    Div(
                                        'Time',
                                        Span(
                                            'Sophie Casey,',
                                            Time('07 Jul 2019', datetime='2019-07-07'),
                                            cls='fs-xs text-muted'
                                        ),
                                        cls='col-12'
                                    ),
                                    cls='row mb-6'
                                ),
                                'Title',
                                P('Cute, but too small', cls='mb-2 fs-lg fw-bold'),
                                'Text',
                                P("Shall good midst can't. Have fill own his multiply the divided. Thing great. Of heaven whose signs.", cls='text-gray-500'),
                                'Footer',
                                Div(
                                    Div('Text', P('Was this review helpful?', cls='mb-0 fs-sm'), cls='col-auto d-none d-lg-block'),
                                    Div(
                                        'Rate',
                                        Div(
                                            A(I('', cls='fe fe-thumbs-up'), href='#', cls='rate-item'),
                                            A(I('', cls='fe fe-thumbs-down'), href='#', cls='rate-item'),
                                            cls='rate'
                                        ),
                                        cls='col-auto me-auto'
                                    ),
                                    Div('Text', P('Comments (1)', cls='mb-0 fs-sm'), cls='col-auto d-none d-lg-block'),
                                    Div('Button', A('Comment', href='#!', cls='btn btn-xs btn-outline-border'), cls='col-auto'),
                                    cls='row align-items-center'
                                ),
                                cls='col-12 col-md-8 col-lg-9 col-xl-10'
                            ),
                            cls='row'
                        ),
                        cls='review-body'
                    ),
                    'Child review',
                    Div(
                        Div(
                            'Content',
                            Div(
                                Div(
                                    'Avatar',
                                    Div(
                                        Span(
                                            I('', cls='fa fa-user'),
                                            cls='avatar-title rounded-circle'
                                        ),
                                        cls='avatar avatar-xxl mb-6 mb-md-0'
                                    ),
                                    cls='col-12 col-md-4 col-lg-3 col-xl-2'
                                ),
                                Div(
                                    'Header',
                                    Div(
                                        Div(
                                            'Rating',
                                            Div(
                                                Div(I('', cls='fas fa-star'), cls='rating-item'),
                                                Div(I('', cls='fas fa-star'), cls='rating-item'),
                                                Div(I('', cls='fas fa-star'), cls='rating-item'),
                                                Div(I('', cls='fas fa-star'), cls='rating-item'),
                                                Div(I('', cls='fas fa-star'), cls='rating-item'),
                                                cls='rating fs-sm text-dark'
                                            ),
                                            cls='col-12'
                                        ),
                                        Div(
                                            'Time',
                                            Span(
                                                'William Stokes,',
                                                Time('14 Jul 2019', datetime='2019-07-14'),
                                                cls='fs-xs text-muted'
                                            ),
                                            cls='col-12'
                                        ),
                                        cls='row mb-6'
                                    ),
                                    'Title',
                                    P('Very good', cls='mb-2 fs-lg fw-bold'),
                                    'Text',
                                    P('Made face lights yielding forth created for image behold blessed seas.', cls='text-gray-500'),
                                    'Footer',
                                    Div(
                                        Div('Text', P('Was this review helpful?', cls='mb-0 fs-sm'), cls='col-auto d-none d-lg-block'),
                                        Div(
                                            'Rate',
                                            Div(
                                                A(I('', cls='fe fe-thumbs-up'), href='#', cls='rate-item'),
                                                A(I('', cls='fe fe-thumbs-down'), href='#', cls='rate-item'),
                                                cls='rate'
                                            ),
                                            cls='col-auto me-auto'
                                        ),
                                        Div('Text', P('Comments (0)', cls='mb-0 fs-sm'), cls='col-auto d-none d-lg-block'),
                                        Div('Button', A('Comment', href='#!', cls='btn btn-xs btn-outline-border'), cls='col-auto'),
                                        cls='row align-items-center'
                                    ),
                                    cls='col-12 col-md-8 col-lg-9 col-xl-10'
                                ),
                                cls='row'
                            ),
                            cls='review-body'
                        ),
                        cls='review review-child'
                    ),
                    cls='review'
                ),
                cls='card-body border'
            ),
            Div(
                Code(
                    '<div class="review">',
                    '<!-- Body -->',
                    '<div class="review-body">',
                    '<div class="row">',
                    '<div class="col-12 col-md-auto">',
                    '<!-- Avatar -->',
                    '<div class="avatar avatar-xxl mb-6 mb-md-0">',
                    '<span class="avatar-title rounded-circle">',
                    '<i class="fa fa-user"></i>',
                    '</span>',
                    '</div>',
                    '</div>',
                    '<div class="col-12 col-md">',
                    '<!-- Header -->',
                    '<div class="row mb-6">',
                    '<div class="col-12">',
                    '<!-- Rating -->',
                    '<div class="rating fs-sm text-dark" data-value="3">',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '<div class="col-12">',
                    '<!-- Time -->',
                    '<span class="fs-xs text-muted">',
                    'Sophie Casey, <time datetime="2019-07-07">07 Jul 2019</time>',
                    '</span>',
                    '</div>',
                    '</div>',
                    '<!-- Title -->',
                    '<p class="mb-2 fs-lg fw-bold">',
                    'Cute, but too small',
                    '</p>',
                    '<!-- Text -->',
                    '<p class="text-gray-500">',
                    "Shall good midst can't. Have fill own his multiply the divided. Thing great. Of heaven whose signs.",
                    '</p>',
                    '<!-- Footer -->',
                    '<div class="row align-items-center">',
                    '<div class="col-auto d-none d-lg-block">',
                    '<!-- Text -->',
                    '<p class="mb-0 fs-sm">Was this review helpful?</p>',
                    '</div>',
                    '<div class="col-auto me-auto">',
                    '<!-- Rate -->',
                    '<div class="rate">',
                    '<a class="rate-item" data-toggle="vote" data-count="2" href="#" role="button">',
                    '<i class="fe fe-thumbs-up"></i>',
                    '</a>',
                    '<a class="rate-item" data-toggle="vote" data-count="1" href="#" role="button">',
                    '<i class="fe fe-thumbs-down"></i>',
                    '</a>',
                    '</div>',
                    '</div>',
                    '<div class="col-auto d-none d-lg-block">',
                    '<!-- Text -->',
                    '<p class="mb-0 fs-sm">Comments (1)</p>',
                    '</div>',
                    '<div class="col-auto">',
                    '<!-- Button -->',
                    '<a class="btn btn-xs btn-outline-border" href="#!">',
                    'Comment',
                    '</a>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '<!-- Child review -->',
                    '<div class="review review-child">',
                    '<div class="review-body">',
                    '<!-- Content -->',
                    '<div class="row">',
                    '<div class="col-12 col-md-auto">',
                    '<!-- Avatar -->',
                    '<div class="avatar avatar-xxl mb-6 mb-md-0">',
                    '<span class="avatar-title rounded-circle">',
                    '<i class="fa fa-user"></i>',
                    '</span>',
                    '</div>',
                    '</div>',
                    '<div class="col-12 col-md">',
                    '<!-- Header -->',
                    '<div class="row mb-6">',
                    '<div class="col-12">',
                    '<!-- Rating -->',
                    '<div class="rating fs-sm text-dark" data-value="4">',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '<div class="rating-item">',
                    '<i class="fas fa-star"></i>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '<div class="col-12">',
                    '<!-- Time -->',
                    '<span class="fs-xs text-muted">',
                    'William Stokes, <time datetime="2019-07-14">14 Jul 2019</time>',
                    '</span>',
                    '</div>',
                    '</div>',
                    '<!-- Title -->',
                    '<p class="mb-2 fs-lg fw-bold">',
                    'Very good',
                    '</p>',
                    '<!-- Text -->',
                    '<p class="text-gray-500">',
                    'Made face lights yielding forth created for image behold blessed seas.',
                    '</p>',
                    '<!-- Footer -->',
                    '<div class="row align-items-center">',
                    '<div class="col-auto d-none d-lg-block">',
                    '<!-- Text -->',
                    '<p class="mb-0 fs-sm">Was this review helpful?</p>',
                    '</div>',
                    '<div class="col-auto me-auto">',
                    '<!-- Rate -->',
                    '<div class="rate">',
                    '<a class="rate-item" data-toggle="vote" data-count="7" href="#" role="button">',
                    '<i class="fe fe-thumbs-up"></i>',
                    '</a>',
                    '<a class="rate-item" data-toggle="vote" data-count="0" href="#" role="button">',
                    '<i class="fe fe-thumbs-down"></i>',
                    '</a>',
                    '</div>',
                    '</div>',
                    '<div class="col-auto d-none d-lg-block">',
                    '<!-- Text -->',
                    '<p class="mb-0 fs-sm">Comments (0)</p>',
                    '</div>',
                    '<div class="col-auto">',
                    '<!-- Button -->',
                    '<a class="btn btn-xs btn-outline-border" href="#!">',
                    'Comment',
                    '</a>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '</div>',
                    '</div>',
                    cls='highlight html'
                ),
                cls='card-footer fs-sm bg-dark'
            ),
            cls='card'
        ),
        cls="px-md-10 py-10"
    )
