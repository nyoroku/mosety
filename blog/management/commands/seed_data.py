"""
Seed data management command for Paradise Boat Rides Naivasha website.
Creates sample Tours, Testimonials, FAQs, Blog Posts, and Services.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bookings.models import Tour
from testimonials.models import Testimonial
from seo.models import FAQ, LocalPage
from blog.models import Post
from services.models import Service

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample data for development'

    def handle(self, *args, **options):
        self.stdout.write('[SEED] Seeding database...\n')
        
        # Create admin user if not exists
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@paradiseboatridesnaivasha.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('[OK] Created admin user'))

        # Create Services
        self.create_services()

        # Create Tours
        self.create_tours()
        
        # Create Testimonials
        self.create_testimonials()
        
        # Create FAQs
        self.create_faqs()
        
        # Create Blog Posts
        self.create_blog_posts(admin)
        
        # Create Local Pages
        self.create_local_pages()

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Database seeded successfully!'))

    def create_services(self):
        services_data = [
            {
                'title': 'Guided Nature Interpretation',
                'slug': 'guided-nature-interpretation',
                'description': 'Professional guide onboard to explain wildlife behavior, bird species, lake ecology, and conservation efforts. Educational, family-friendly, and premium experience for curious minds.',
                'icon_class': 'fas fa-binoculars',
                'is_active': True,
                'order': 1,
            },
            {
                'title': 'School Educational Tours',
                'slug': 'school-educational-tours',
                'description': 'Safe, guided educational boat experiences for schools and universities. Designed to combine learning with adventure in a controlled, supervised environment with curriculum-aligned content.',
                'icon_class': 'fas fa-graduation-cap',
                'is_active': True,
                'order': 2,
            },
            {
                'title': 'Corporate Team-Building',
                'slug': 'corporate-team-building',
                'description': 'Boat transport and lake activities for companies doing off-sites, strategy days, or staff retreats. Includes multiple boat trips, branded experiences, and catering coordination.',
                'icon_class': 'fas fa-users',
                'is_active': True,
                'order': 3,
            },
            {
                'title': 'Photography & Filming',
                'slug': 'photography-filming',
                'description': 'Specialized boat positioning for photographers and film crews. Stable platforms, optimal timing for golden hour, and expert knowledge of the best wildlife spots for stunning shots.',
                'icon_class': 'fas fa-camera',
                'is_active': True,
                'order': 4,
            },
            {
                'title': 'Wedding & Events',
                'slug': 'wedding-events',
                'description': 'Make your special day unforgettable with lakeside celebrations. We provide decorated boats for wedding parties, proposals, anniversaries, and private romantic experiences.',
                'icon_class': 'fas fa-heart',
                'is_active': True,
                'order': 5,
            },
            {
                'title': 'Fishing Expeditions',
                'slug': 'fishing-expeditions',
                'description': 'Join local fishermen for an authentic Lake Naivasha fishing experience. Learn traditional techniques, catch tilapia and black bass, and enjoy a true taste of lakeside life.',
                'icon_class': 'fas fa-fish',
                'is_active': True,
                'order': 6,
            },
        ]

        for service_data in services_data:
            service, created = Service.objects.update_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'  [+] Created service: {service.title}')
            else:
                self.stdout.write(f'  [~] Updated service: {service.title}')

    def create_tours(self):
        tours_data = [
            {
                'name': 'Hippo & Bird Safari',
                'slug': 'hippo-bird-safari',
                'description': '''
                <p>Embark on the ultimate Lake Naivasha wildlife experience! Our Hippo & Bird Safari takes you through the most scenic parts of the lake, where you'll encounter pods of hippos in their natural habitat and over 400 species of birds.</p>
                
                <h3>What to Expect</h3>
                <ul>
                    <li>Close encounters with hippos (at safe distances)</li>
                    <li>Fish eagles, pelicans, cormorants, and herons</li>
                    <li>Expert guide narration on wildlife behavior</li>
                    <li>Photo opportunities at every turn</li>
                </ul>
                
                <p>Perfect for families, photographers, and nature enthusiasts. This is our most popular tour for a reason!</p>
                ''',
                'highlights': 'Hippo pods up close\nFish eagle sightings\nExpert wildlife guide\nPerfect for photography',
                'location': 'Lake Naivasha',
                'duration_hours': 2.0,
                'price_per_person': 2500,
                'max_people': 8,
                'is_active': True,
            },
            {
                'name': 'Sunset Cruise',
                'slug': 'sunset-cruise',
                'description': '''
                <p>Experience the magic of Lake Naivasha as the sun dips below the horizon. Our Sunset Cruise is a romantic, peaceful journey perfect for couples, photographers, or anyone seeking a moment of tranquility.</p>
                
                <h3>The Experience</h3>
                <ul>
                    <li>Golden hour photography opportunities</li>
                    <li>Calm evening waters</li>
                    <li>Hippos emerging for evening grazing</li>
                    <li>Stunning views of the Aberdare Mountains</li>
                </ul>
                
                <p>Light refreshments available. The perfect end to a day in Naivasha.</p>
                ''',
                'highlights': 'Golden sunset views\nRomantic atmosphere\nEvening wildlife activity\nMountain backdrop',
                'location': 'Lake Naivasha',
                'duration_hours': 1.5,
                'price_per_person': 3000,
                'max_people': 6,
                'is_active': True,
            },
            {
                'name': 'Crescent Island Walking Safari',
                'slug': 'crescent-island-walk',
                'description': '''
                <p>Combine a scenic boat ride with a walking safari on Crescent Island—one of Kenya's few places where you can walk freely among giraffes, zebras, wildebeest, and other wildlife.</p>
                
                <h3>Your Adventure Includes</h3>
                <ul>
                    <li>Boat transfer to Crescent Island</li>
                    <li>1-hour guided walking safari</li>
                    <li>Walk among giraffes and zebras</li>
                    <li>No predators—completely safe</li>
                    <li>Spectacular photo opportunities</li>
                </ul>
                
                <p>Note: Crescent Island entry fee (KES 430 for Kenyan residents / $30 for non-residents) is payable separately at the gate.</p>
                ''',
                'highlights': 'Walk among giraffes\nNo predators - safe for all ages\nBoat transfer included\nGuided experience',
                'location': 'Crescent Island',
                'duration_hours': 3.0,
                'price_per_person': 3500,
                'max_people': 10,
                'is_active': True,
            },
            {
                'name': 'Full Day Lake Adventure',
                'slug': 'full-day-adventure',
                'description': '''
                <p>The complete Lake Naivasha experience! Spend an entire day exploring the lake's hidden gems, from papyrus channels to secret islands, with breaks for lunch and relaxation.</p>
                
                <h3>Full Day Includes</h3>
                <ul>
                    <li>Morning hippo & bird safari</li>
                    <li>Visit to Crescent Island</li>
                    <li>Lunch break at lakeside restaurant</li>
                    <li>Afternoon exploration of hidden channels</li>
                    <li>Sunset cruise to end the day</li>
                </ul>
                
                <p>Lunch and island entry fees not included. Perfect for those wanting the complete experience.</p>
                ''',
                'highlights': 'Complete lake experience\nMultiple activities\nSunrise to sunset\nHidden gems revealed',
                'location': 'Lake Naivasha',
                'duration_hours': 8.0,
                'price_per_person': 8000,
                'max_people': 6,
                'is_active': True,
            },
            {
                'name': 'Private Charter',
                'slug': 'private-charter',
                'description': '''
                <p>Exclusive boat hire for your group. Whether it's a birthday celebration, proposal, corporate outing, or just quality time with loved ones—we customize everything to your needs.</p>
                
                <h3>Private Charter Benefits</h3>
                <ul>
                    <li>Exclusive boat for your party</li>
                    <li>Flexible timing and route</li>
                    <li>Custom activities and stops</li>
                    <li>Special requests accommodated</li>
                    <li>Photography packages available</li>
                </ul>
                
                <p>Contact us to discuss your requirements. We can arrange everything from champagne to live music.</p>
                ''',
                'highlights': 'Fully private experience\nCustom itinerary\nSpecial occasions welcome\nFlexible scheduling',
                'location': 'Lake Naivasha',
                'duration_hours': 2.0,
                'price_per_person': 15000,
                'max_people': 8,
                'is_active': True,
            },
            {
                'name': 'Photography Safari',
                'slug': 'photography-safari',
                'description': '''
                <p>Designed specifically for photographers, this specialized tour focuses on finding the best light, angles, and wildlife moments. Our captain knows exactly where to position the boat for that perfect shot.</p>
                
                <h3>For Photographers</h3>
                <ul>
                    <li>Golden hour timing options</li>
                    <li>Slow boat movements for stable shots</li>
                    <li>Wildlife behavior expertise</li>
                    <li>Bird nesting site visits</li>
                    <li>Drone-friendly zones (with permits)</li>
                </ul>
                
                <p>Bring your gear—we'll get you the shots. All skill levels welcome.</p>
                ''',
                'highlights': 'Optimized for photography\nGolden hour timing\nStable boat positioning\nExpert wildlife guidance',
                'location': 'Lake Naivasha',
                'duration_hours': 3.0,
                'price_per_person': 4000,
                'max_people': 4,
                'is_active': True,
            },
        ]

        for tour_data in tours_data:
            tour, created = Tour.objects.update_or_create(
                slug=tour_data['slug'],
                defaults=tour_data
            )
            if created:
                self.stdout.write(f'  [+] Created tour: {tour.name}')
            else:
                self.stdout.write(f'  [~] Updated tour: {tour.name}')

    def create_testimonials(self):
        testimonials_data = [
            {
                'customer_name': 'Sarah Mitchell',
                'customer_country': 'United Kingdom',
                'rating': 5,
                'testimonial_text': 'Absolutely magical experience! The hippos came so close to our boat, and the birdlife was incredible. Our guide knew so much about the wildlife. Already planning our next visit!',
                'is_active': True,
                'is_featured': True,
            },
            {
                'customer_name': 'Michael Chen',
                'customer_country': 'Singapore',
                'rating': 5,
                'testimonial_text': 'The sunset cruise exceeded all expectations. Golden skies, peaceful waters, and hippos emerging in the evening light. A photographer\'s dream!',
                'is_active': True,
                'is_featured': True,
            },
            {
                'customer_name': 'Emma & James Wilson',
                'customer_country': 'Australia',
                'rating': 5,
                'testimonial_text': 'We did the Crescent Island combo and loved every minute. Walking among giraffes felt surreal! The boat ride there was equally stunning.',
                'is_active': True,
                'is_featured': True,
            },
            {
                'customer_name': 'David Omondi',
                'customer_country': 'Kenya',
                'rating': 5,
                'testimonial_text': 'As a Kenyan, I\'m proud of this kind of service. Professional, punctual, and genuinely passionate about Lake Naivasha. Highly recommended!',
                'is_active': True,
                'is_featured': True,
            },
            {
                'customer_name': 'Maria Fernandez',
                'customer_country': 'Spain',
                'rating': 5,
                'testimonial_text': 'Our family of four had the best day on the lake. The kids loved the hippos and the guides made sure everyone was safe and having fun.',
                'is_active': True,
                'is_featured': False,
            },
            {
                'customer_name': 'Thomas Mueller',
                'customer_country': 'Germany',
                'rating': 5,
                'testimonial_text': 'Booked a private charter for my wife\'s birthday. They arranged everything perfectly—even had cake on board! Unforgettable day.',
                'is_active': True,
                'is_featured': False,
            },
            {
                'customer_name': 'Angela and Paul Keen',
                'customer_country': 'England',
                'rating': 5,
                'testimonial_text': 'We did the sunset cruise and it was magical. Calm water, soft music, golden sky — it felt like a movie scene. The crew gave us space but stayed attentive. 10/10.',
                'is_active': True,
                'is_featured': True,
            },
            {
                'customer_name': 'Michael T',
                'customer_country': 'California, USA',
                'rating': 5,
                'testimonial_text': 'I\'ve done boat tours all over the world, but this one in Naivasha stands out. The team was punctual, knowledgeable, and the wildlife sightings were incredible.',
                'is_active': True,
                'is_featured': True,
            },
        ]

        for i, test_data in enumerate(testimonials_data):
            test_data['order'] = i
            testimonial, created = Testimonial.objects.update_or_create(
                customer_name=test_data['customer_name'],
                defaults=test_data
            )
            if created:
                self.stdout.write(f'  [+] Created testimonial: {testimonial.customer_name}')

    def create_faqs(self):
        faqs_data = [
            {
                'question': 'Do you offer private boat rides in Naivasha?',
                'answer': '<p>Yes! We offer private boat charters for couples, families, corporate groups, and special occasions. You get the entire boat to yourself with a customized itinerary. Contact us via WhatsApp to discuss your requirements.</p>',
                'plain_answer': 'Yes, we offer private boat charters for couples, families, and groups with customized itineraries.',
                'is_active': True,
                'order': 1,
            },
            {
                'question': 'What wildlife can I see during a Lake Naivasha boat ride?',
                'answer': '<p>Lake Naivasha is home to large pods of hippos, over 400 bird species (including fish eagles, pelicans, and cormorants), and if you visit Crescent Island, you can walk among giraffes, zebras, and wildebeest. The lake also supports a variety of fish species.</p>',
                'plain_answer': 'You can see hippos, fish eagles, pelicans, cormorants, and over 400 bird species. Crescent Island has giraffes and zebras.',
                'is_active': True,
                'order': 2,
            },
            {
                'question': 'How do I book a boat ride with Paradise Boat Rides Naivasha?',
                'answer': '<p>Booking is easy! You can:</p><ul><li>WhatsApp us directly at +254 791 734 268</li><li>Use our online booking form</li><li>Call us to reserve your spot</li></ul><p>We recommend booking at least 24 hours in advance, especially for weekends and holidays.</p>',
                'plain_answer': 'Book via WhatsApp (+254 791 734 268), online form, or phone. We recommend 24 hours advance booking.',
                'is_active': True,
                'order': 3,
            },
            {
                'question': 'What types of boat rides do you offer on Lake Naivasha?',
                'answer': '<p>We offer several tour options:</p><ul><li><strong>Hippo & Bird Safari</strong> - Wildlife spotting (2 hours)</li><li><strong>Sunset Cruise</strong> - Golden hour experience (1.5 hours)</li><li><strong>Crescent Island Combo</strong> - Boat + walking safari (3 hours)</li><li><strong>Photography Safari</strong> - Optimized for photographers (3 hours)</li><li><strong>Full Day Adventure</strong> - Complete lake experience (8 hours)</li><li><strong>Private Charter</strong> - Exclusive customized tours</li></ul>',
                'plain_answer': 'We offer Hippo Safari, Sunset Cruise, Crescent Island tours, Photography Safari, Full Day Adventure, and Private Charters.',
                'is_active': True,
                'order': 4,
            },
            {
                'question': 'Do you offer sunset cruises on Lake Naivasha?',
                'answer': '<p>Absolutely! Our Sunset Cruise is one of our most popular experiences. You\'ll enjoy the magical golden hour as hippos emerge for evening grazing, with stunning views of the Aberdare Mountains. Perfect for couples and photographers.</p>',
                'plain_answer': 'Yes, our Sunset Cruise features golden hour views, evening hippo activity, and mountain backdrops.',
                'is_active': True,
                'order': 5,
            },
            {
                'question': 'Is it safe to go on a boat ride at Lake Naivasha?',
                'answer': '<p>Safety is our top priority. All our boats are equipped with:</p><ul><li>Quality life jackets for all passengers</li><li>First aid kits</li><li>Experienced, licensed captains</li><li>Regular boat maintenance</li></ul><p>We maintain safe distances from hippos while still providing excellent viewing opportunities.</p>',
                'plain_answer': 'Yes, we prioritize safety with life jackets, first aid kits, licensed captains, and maintained boats.',
                'is_active': True,
                'order': 6,
            },
            {
                'question': 'What is the best time for a boat ride on Lake Naivasha?',
                'answer': '<p>Early morning (6:00-9:00 AM) and late afternoon (4:00-6:30 PM) are ideal for:</p><ul><li>Cooler temperatures</li><li>Best wildlife activity</li><li>Optimal photography light</li><li>Calmer waters</li></ul><p>Midday rides are also available but can be warmer with less wildlife activity.</p>',
                'plain_answer': 'Early morning (6-9 AM) and late afternoon (4-6:30 PM) offer the best wildlife activity and photography light.',
                'is_active': True,
                'order': 7,
            },
            {
                'question': 'What should I bring for a Lake Naivasha boat ride?',
                'answer': '<p>We recommend bringing:</p><ul><li>Sunscreen and sunglasses</li><li>Hat or cap</li><li>Camera (waterproof bag recommended)</li><li>Binoculars for birdwatching</li><li>Light jacket for morning/evening</li><li>Water bottle</li></ul><p>We provide life jackets and basic first aid.</p>',
                'plain_answer': 'Bring sunscreen, sunglasses, hat, camera, binoculars, light jacket, and water. We provide life jackets.',
                'is_active': True,
                'order': 8,
            },
        ]

        for faq_data in faqs_data:
            faq, created = FAQ.objects.update_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'  [+] Created FAQ: {faq.question[:50]}...')

    def create_blog_posts(self, author):
        posts_data = [
            {
                'title': 'Best Boat Ride in Kenya: Why Lake Naivasha Tops Every List',
                'slug': 'best-boat-ride-kenya-lake-naivasha',
                'content': '''
                <p>When travelers ask about the best boat ride experiences in Kenya, Lake Naivasha consistently emerges as the top destination. Here's why this stunning freshwater lake offers an unmatched boating experience.</p>
                
                <h2>The Wildlife Factor</h2>
                <p>Unlike coastal boat rides, Lake Naivasha puts you in the heart of African wildlife. Hippo pods, fish eagles, pelicans, and over 400 bird species make every trip a mobile safari.</p>
                
                <h2>Accessibility from Nairobi</h2>
                <p>Just 90 minutes from Nairobi, Lake Naivasha is perfect for day trips. No flights, no long drives—just pure escape.</p>
                
                <h2>Year-Round Availability</h2>
                <p>The lake offers excellent conditions throughout the year, though early morning and late afternoon trips are recommended for wildlife activity and photography.</p>
                
                <h2>Book Your Experience</h2>
                <p>Ready to experience Kenya's best boat ride? Contact Paradise Boat Rides Naivasha for instant WhatsApp booking.</p>
                ''',
                'meta_description': 'Discover why Lake Naivasha offers Kenya\'s best boat ride experience. Wildlife, accessibility, and year-round beauty make it the top choice.',
                'status': 'published',
            },
            {
                'title': 'Boat Ride Naivasha: The Ultimate 2025 Guide',
                'slug': 'boat-ride-naivasha-guide-2025',
                'content': '''
                <p>Planning a boat ride at Lake Naivasha in 2025? This comprehensive guide covers everything you need to know for an unforgettable experience.</p>
                
                <h2>Best Time to Visit</h2>
                <p>Early morning (6-9 AM) and late afternoon (4-6:30 PM) offer the best wildlife sightings and photography conditions.</p>
                
                <h2>What You'll See</h2>
                <ul>
                    <li>Hippo pods (some as large as 30+)</li>
                    <li>Fish eagles hunting</li>
                    <li>Pelican colonies</li>
                    <li>Cormorants and herons</li>
                    <li>Mountain views</li>
                </ul>
                
                <h2>Pricing Guide 2025</h2>
                <p>Tours range from KES 2,500 for a standard safari to KES 15,000 for private charters. Crescent Island entry fees are separate.</p>
                
                <h2>How to Book</h2>
                <p>The easiest way is WhatsApp booking with Paradise Boat Rides Naivasha. Instant confirmation, flexible timing, and local expertise.</p>
                ''',
                'meta_description': 'Complete 2025 guide to Lake Naivasha boat rides. Prices, timing, wildlife, and booking tips from local experts.',
                'status': 'published',
            },
            {
                'title': 'Planning Your Complete Kenya Adventure? Partner with Guru Adventures',
                'slug': 'kenya-adventure-guru-adventures-safari',
                'content': '''
                <p>While Lake Naivasha is a must-visit destination, Kenya offers so much more. If you're planning a complete Kenya adventure, consider partnering with safari experts for a seamless experience.</p>
                
                <h2>Beyond the Lake</h2>
                <p>Combine your Naivasha boat ride with:</p>
                <ul>
                    <li>Masai Mara safari</li>
                    <li>Hell's Gate cycling</li>
                    <li>Amboseli elephant viewing</li>
                    <li>Samburu wilderness</li>
                </ul>
                
                <h2>Multi-Day Itineraries</h2>
                <p>A well-planned Kenya trip often includes Lake Naivasha as a relaxing break between safari parks. The lake's proximity to Nairobi makes it an ideal first or last stop.</p>
                
                <h2>Book Smart</h2>
                <p>For lake experiences, book directly with local operators like Paradise Boat Rides Naivasha for the best rates and authentic experiences.</p>
                ''',
                'meta_description': 'Plan your complete Kenya adventure. Combine Lake Naivasha boat rides with Masai Mara, Amboseli, and more.',
                'status': 'published',
            },
        ]

        for post_data in posts_data:
            post_data['author'] = author
            post, created = Post.objects.update_or_create(
                slug=post_data['slug'],
                defaults=post_data
            )
            if created:
                self.stdout.write(f'  [+] Created blog post: {post.title[:50]}...')

    def create_local_pages(self):
        pages_data = [
            {
                'title': 'Boat Rides Naivasha',
                'slug': 'boat-rides-naivasha',
                'seo_title': 'Boat Rides Naivasha | Best Lake Experiences | Paradise Boat Rides Naivasha',
                'meta_description': 'Book the best boat rides in Naivasha. Hippo safaris, sunset cruises, and Crescent Island tours with experienced local guides.',
                'primary_keyword': 'boat rides naivasha',
                'location': 'Lake Naivasha',
                'content': '<p>Experience Lake Naivasha on the best boat rides available. Our experienced guides take you to the most scenic spots, hippo pods, and bird colonies.</p>',
                'is_active': True,
            },
            {
                'title': 'Crescent Island Tours',
                'slug': 'crescent-island-tours',
                'seo_title': 'Crescent Island Tours | Walking Safari Naivasha | Paradise Boat Rides Naivasha',
                'meta_description': 'Visit Crescent Island by boat and walk among giraffes and zebras. Safe, guided experiences from Lake Naivasha.',
                'primary_keyword': 'crescent island tours',
                'location': 'Crescent Island',
                'content': '<p>Crescent Island is where you can actually walk among African wildlife. We provide boat transfers and can arrange guided walks.</p>',
                'is_active': True,
            },
            {
                'title': 'Sunset Cruises Naivasha',
                'slug': 'sunset-cruises-naivasha',
                'seo_title': 'Sunset Cruises Naivasha | Romantic Lake Experiences | Paradise Boat Rides Naivasha',
                'meta_description': 'Book a magical sunset cruise on Lake Naivasha. Golden hour photography, hippo viewing, and mountain views.',
                'primary_keyword': 'sunset cruises naivasha',
                'location': 'Lake Naivasha',
                'content': '<p>Our sunset cruises are perfect for couples, photographers, or anyone seeking tranquility as the sun sets over Lake Naivasha.</p>',
                'is_active': True,
            },
        ]

        for page_data in pages_data:
            page, created = LocalPage.objects.update_or_create(
                slug=page_data['slug'],
                defaults=page_data
            )
            if created:
                self.stdout.write(f'  [+] Created local page: {page.title}')
