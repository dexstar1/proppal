from fasthtml.common import *

def Map():
    return Section(
        H3('Map'),
        P(
            'Adds an interactive map powered by Google Maps. Make sure to replace the default Google Maps API key in',
            Code('src/partials/script.html'),
            'with your custom one to enable maps on your local server or custom domain.',
            A('Plugin documentation', href='https://cloud.google.com/maps-platform/?utm_source=google&utm_medium=cpc&utm_campaign=FY18-Q2-global-demandgen-paidsearchonnetworkhouseads-cs-maps_contactsal_saf&utm_content=text-ad-none-none-DEV_c-CRE_269776056235-ADGP_Hybrid+%7C+AW+SEM+%7C+BKWS+~+EXA_%5BM:1%5D_EMEAOt_EN_Converters_API-KWID_43700027750115852-kwd-313687199737-userloc_2752&utm_term=KW_google%20mapping%20api-ST_google+mapping+api&gclid=EAIaIQobChMI2JDW_JGL5gIVx4KyCh3tSAvbEAAYASAAEgLivPD_BwE'),
            cls='text-gray-500'
        ),
        Code('data-map'),
        '- initializes the map plugin.',
        Code('data-zoom'),
        '- initial map zooming level. Ignore if you want to allow the map scale automatically to show all markers specified in the',
        Code('data-marker'),
        'attribute.',
        Code('data-markers'),
        '- an array of objects with markers info. E.g.',
        Code('data-markers=\'[{"position": [53.5508748,9.9985808], "info": "Popup content."}]\''), '.',
        Div(
            Div(
                Div(
                    Div('', cls='ratio-item'),
                    cls='ratio ratio-21x9'
                ),
                cls='card-body border'
            ),
            Div(
                Code(
                    '<div class="ratio ratio-21x9">',
                    '<div class="ratio-item" data-map',
                    'data-markers=\'[{"position": [53.5508748,9.9985808], "info": "<div class=\\"card card-sm\\"><div class=\\"card-body\\"><p class=\\"mb-2 fw-bold\\">Baldwin Hills Crenshaw Plaza</p><p class=\\"mb-3 text-gray-500\\">Mönckebergstrasse 11 20095 Hamburg, Germany</p><p class=\\"mb-1 fw-bold\\">Phone:</p><p class=\\"mb-3 text-grat-500\\">6-146-389-574</p><p class=\\"mb-1 fw-bold\\">Store Hours:</p><p class=\\"mb-0 text-grat-500\\">10 am - 10 pm EST, 7 days a week</p></div>"}, {"position": [45.4646477,9.1935083], "info": "<div class=\\"card card-sm\\"><div class=\\"card-body\\"><p class=\\"mb-2 fw-bold\\">Stonewood Center</p><p class=\\"mb-3 text-gray-500\\">Largo Corsia Dei Servi 3 20122 Milan, Italy</p><p class=\\"mb-1 fw-bold\\">Phone:</p><p class=\\"mb-3 text-grat-500\\">6-146-389-574</p><p class=\\"mb-1 fw-bold\\">Store Hours:</p><p class=\\"mb-0 text-grat-500\\">10 am - 10 pm EST, 7 days a week</p></div>"}, {"position": [53.332769,-6.2663917], "info": "<div class=\\"card card-sm\\"><div class=\\"card-body\\"><p class=\\"mb-2 fw-bold\\">Shalyapin Palace</p><p class=\\"mb-3 text-gray-500\\">Block 5, 5th Floor, Harcourt Centre, Harcourt Road Dublin, Ireland</p><p class=\\"mb-1 fw-bold\\">Phone:</p><p class=\\"mb-3 text-grat-500\\">6-146-389-574</p><p class=\\"mb-1 fw-bold\\">Store Hours:</p><p class=\\"mb-0 text-grat-500\\">10 am - 10 pm EST, 7 days a week</p></div>"}]\'>',
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
