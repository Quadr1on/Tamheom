from flask import Flask
from models import db
from routes import main
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main)
    
    return app

def init_db():
    app = create_app()
    with app.app_context():
            # Drop all tables first to avoid any existing table issues
            db.drop_all()
            # Create all tables
            db.create_all()
            
            # Add sample data
            from models import City, Experience
            
            # Add sample cities
            
            chennai = City(name='Chennai', state='Tamil Nadu', country='India')
            banglore = City(name='Banglore', state='Karnataka', country='India')
            mumbai = City(name='Mumbai', state='Maharashtra', country='India')
            lucknow = City(name='Lucknow', state='Uttar Pradesh', country='India')
            delhi = City(name='Delhi',state='Delhi',country='India')

            db.session.add_all([chennai,delhi,mumbai,banglore,lucknow])
            db.session.commit()  # Commit cities first
            
            # Add sample experiences for NYC
            #types = [local_event,hidden_gems,walking_tour]
            '''
            Experience(
                    name='Event_name',
                    type='<local_event,hidden_gem,walking_tour>',
                    description='NULL',
                    city_id=<City>.id,
                    details={'time': '<Month DD - time>', 'location': '<Location>'}
                    details={'type': 'Restaurant', 'price_range': '$$'}
                    details={'distance': '2.5 miles', 'distance': '2 hours'}
                )
            '''
            experiences = [
                Experience(
                    name='Samay Raina Unfiltered.',
                    type='local_event',
                    description='Stand-up comedy',
                    city_id=chennai.id,
                    details={'time': 'Sun 17 Nov 2024 7:00pm', 'location': 'The Music Academy'}
                ),
                Experience(
                    name='Tribute to Coldplay',
                    type='local_event',
                    description='Art festival featuring global artist',
                    city_id=chennai.id,
                    details={'time': 'Sun 1 Dec 2024', 'location': 'yet to announced'}
                ),
                Experience(
                    name='Arman Malik Concert',
                    type='local_event',
                    description='Annual street art festival featuring local artists',
                    city_id=chennai.id,
                    details={'time': 'December 22nd - 6PM', 'location': 'YMCA, Royapettah'}
                ),
                Experience(
                    name='Pulusu Rachulu',
                    type='hidden_gem',
                    description='NULL',
                    city_id=chennai.id,
                    details={'type':'Resturant'}
                ),
                Experience(
                    name='Muttukadu Lake',
                    type='hidden_gem',
                    description='NULL',
                    city_id=chennai.id,
                    details={'type': 'Tourist Spot', 'Location': 'East Coast Road'}
                ),
                Experience(
                    name='Writers Cafe',
                    type='hidden_gem',
                    description='Cafe for book lovers',
                    city_id=chennai.id,
                    details={'type':'Cafe'}
                ),
                Experience(
                    name='SRM Vadapalni',
                    type='hidden_gem',
                    description='Explore colonial-era buildings',
                    city_id=chennai.id,
                    details={'type':'University'}
                ),
            Experience(
                    name='Mylapore Walk',
                    type='walking_tour',
                    description='Cultural Walk',
                    city_id=chennai.id,
                    details={'distance': '4 KM'}
                ),
                Experience(
                    name='Marina Beach',
                    type='walking_tour',
                    description='A place to enjoy the sunset',
                    city_id=chennai.id,
                    details={'distance': '13 KM'}
                ),
                Experience(
                    name='George Town Origins',
                    type='walking_tour',
                    description='Explore colonial-era buildings',
                    city_id=chennai.id,
                    details={'distance': '12.7 KM'}
                ),

                Experience(
                    name='Diljit Dosanjh Tour 2024',
                    type='local_event',
                    description='Diljit Dosanjh Concert',
                    city_id=lucknow.id,
                    details={'time': '22 Nov 2024', 'location': 'To be announced'}
                ),
                Experience(
                    name='Shreya Ghoshal - All Hearts Tour',
                    type='local_event',
                    description='Shreya Ghoshal concert',
                    city_id=lucknow.id,
                    details={'time': '21 Dec 2024', 'location': 'Yet To Be Announced'}
                ),
                Experience(
                    name='McDowells Soda Yaari Jam Anuv Jain and Zaeden ',
                    type='local_event',
                    description='Meet-Up',
                    city_id=lucknow.id,
                    details={'time': '12 Jan 2025', 'location': 'Yet To Be Announced'}
                
                ),
                    
                Experience(
                    name='Cafe 1991',
                    type='hidden_gem',
                    description='Hidden cafe with amazing atmosphere',
                    city_id=lucknow.id,
                    details={'type': 'Cafe'}
                ),
                Experience(
                    name='Lok Kala Sangrahalaya',
                    type='hidden_gem',
                    description='Art and Craft Mueseum',
                    city_id=lucknow.id,
                    details={'type': 'Mueseum'}
                ),
                Experience(
                    name='Kudiya Ghat',
                    type='hidden_gem',
                    description='NULL',
                    city_id=lucknow.id,
                    details={'type': 'Lake'}
                ),
                Experience(
                    name='Janeshwar Mishra Park',
                    type='walking_tour',
                    description='NULL',
                    city_id=lucknow.id,
                    details={'distance': '1.52 sq km'}
                ),
                Experience(
                    name='Gomti Riverfront',
                    type='walking_tour',
                    description='Explore the beautiful banks of river Gomti',
                    city_id=lucknow.id,
                    details={'distance': '12 km'}
                ),
                Experience(
                    name='1090 chauraha',
                    type='walking_tour',
                    description='NULL',
                    city_id=lucknow.id,
                    details={'distance': 'Undefined'}
                ),
                Experience(
                    name='Hazratganj',
                    type='walking_tour',
                    description='Explore the downtown area',
                    city_id=lucknow.id,
                    details={'distance': 'Undefined'}
                ),
                Experience(
                    name='Zakir Khan Live' ,
                    type='local_event',
                    description='Zakir Khan Live',
                    city_id=mumbai.id,
                    details={'time': '3 Nov 2024', 'location': 'Bal ghandharva Rang Mandir,Bandra'}
                ),
                Experience(
                    name='THE JAMIE LEVER SHOW',
                    type='local_event',
                    description='THE JAMIE LEVER SHOW',
                    city_id=mumbai.id,
                    details={'time': '10 Nov 2024', 'location': 'Dinanath Mangeshkar Natyagruha: Vile Parle'}
                ),
                Experience(
                    name='Shankar Mahadevan Live',
                    type='local_event',
                    description='Pop concert',
                    city_id=mumbai.id,
                    details={'time': '20 Dec 2024', 'location': 'Yet To Be Announced','duration': '3 hours'}
                ),
                Experience(
                    name='Kunal Kamra Live',
                    type='local_event',
                    description='Kunal Kamra Live',
                    city_id=mumbai.id,
                    details={'time': '29 Dec 2024', 'location': 'Yet To Be Announced'}
                ),
                Experience(
                    name='Khotachiwadi',
                    type='hidden_gem',
                    description='quaint heritage village',
                    city_id=mumbai.id,
                    details={'type': 'village'}
                ),
                Experience(
                    name='Nehru Science Centre',
                    type='hidden_gem',
                    description=' A great spot for families, this interactive science museum features engaging exhibits and an impressive planetarium',
                    city_id=mumbai.id,
                    details={'distance': '2 hours'}
                ),
                Experience(
                    name='Banganga Tank',
                    type='hidden_gem',
                    description='An ancient water tank surrounded by temples, offering a glimpse into the city’s history and spiritual life',
                    city_id=mumbai.id,
                    details={'duration': '3 hours'}
                ),
                Experience(
                    name='Dharavi',
                    type='walking_tour',
                    description='Dharavi has a vibrant community and interesting entrepreneurial ventures. Guided tours can provide a deeper understanding of this area.',
                    city_id=mumbai.id,
                    details={'distance': '2.4km^2'}
                ),
                Experience(
                    name='Versova Beach',
                    type='walking_tour',
                    description='Quieter than the more famous Juhu Beach, Versova offers a laid-back atmosphere and stunning sunsets',
                    city_id=mumbai.id,
                    details={'distance': 'Undefined'}
                ),
                Experience(
                    name='NH7 Weekender Delhi' ,
                    type='local_event',
                    description='A popular music festival featuring a lineup of local and international artists across various genres',
                    city_id=delhi.id,
                    details={'time': 'November 3-5, 2024', 'location': 'Oysters Beach Water Park, Gurugram'}
                ),
                Experience(
                    name='Bismil Ki Mehfil - Live in Delhi',
                    type='local_event',
                    description='classical music concert',
                    city_id=delhi.id,
                    details={'time': 'November 9, 2024', 'location': 'KD Jadhav Indoor Hall, Delhi'}
                ),
                Experience(
                    name='Piyush Mishra Live in Concert ',
                    type='local_event',
                    description='A musical event featuring performances by various artists',
                    city_id=delhi.id,
                    details={'time': 'November 9, 2024', 'location': 'KD Jadhav Indoor Hall, Delhi'}
                ),
                Experience(
                    name='MindFool India Tour - Vir Das',
                    type='local_event',
                    description='comedy concert',
                    city_id=delhi.id,
                    details={'date': 'November 1, 2024', 'location': 'Sirifort Auditorium, Delhi'}
                ),
                Experience(
                    name='Kisi Ko Batana Mat - Anubhav Singh Bassi',
                    type='local_event',
                    description='comedy concert',
                    city_id=delhi.id,
                    details={'date': 'November 2, 2024', 'location': 'Talkatora Stadium, Delhi'}
                ),
                Experience(
                    name='Gaurav Kapoor LIVE',
                    type='local_event',
                    description='Comedy Concert',
                    city_id=delhi.id,
                    details={'date': 'November 3, 2024', 'location': 'Kamani Auditorium, Delhi'}
                ),
                Experience(
                    name='Agrasen ki Baoli',
                    type='hidden_gem',
                    description='A historical step-well dating back to the 10th century, featuring ornate stone details and arched walls.',
                    city_id=delhi.id,
                    details={'type': 'historical step-well'}
                ),
                Experience(
                    name='Bhuli Bhatiyari Ka Mahal',
                    type='walking_tour',
                    description='Remains of a 14th-century royal hunting lodge, rumored to be haunted.',
                    city_id=delhi.id,
                    details={'type': 'haunted royal hunting lodge'}
                ),
                Experience(
                    name='Tughlakabad Fort',
                    type='hidden_gem',
                    description='Remnants of a stone fort from the Tughlaq period with intact ramparts and battlements.',
                    city_id=delhi.id,
                    details={'type': 'fort'}
                ),
                Experience(
                    name='The Hidden Hour (Escape Rooms)',
                    type='hidden_gem',
                    description='A unique escape room experience located in Hauz Khas Village',
                    city_id=delhi.id,
                    details={'type': 'Escape Rooms'}
                ),
                Experience(
                    name='Jahaz Mahal',
                    type='walking_tour',
                    description='Description: A 15th to 16th-century retreat with domed towers and a courtyard that was once used for flower festivals.',
                    city_id=delhi.id,
                    details={'type': 'mahal'}
                ),
                Experience(
                    name='Satpula Bridge',
                    type='walking_tour',
                    description='Known as the "Seven Arch Bridge," it served as a water harvesting dam and a defense wall during the Tughlaq era.',
                    city_id=delhi.id,
                    details={'type': 'water harvesting dam'}
                ),
                Experience(
                    name='Bangalore Literature Festival',
                    type='local_event',
                    description='Literature festival in Bangalore is a celebration of the rich and varied literary traditions of the city. The festival brings together writers, poets, and artists from across the city to share their thoughts and ideas on literature, art, and culture. The festival is held annually in different locations across the city, and features a wide range of literary genres, including poetry, fiction, drama, and historical fiction. The festival is a great way to enjoy a wide range of literary experiences and connect with other like-minded people.',
                    city_id=banglore.id,
                    details={'time': 'October 28-29, 2024', 'location': 'The Lalit Ashok, Bangalore'}
                ),
                Experience(
                    name='The Great Indian Food Festival',
                    type='local_event',
                    description='Great Indian Food Festival is a celebration of the rich and varied cuisine of the Indian subcontinent. The festival brings together Indian chefs, cooks, and restaurateurs from across the country to share their delicious cuisine with the locals. The festival is held annually in different locations across the country, and features a wide range of cuisines, including North Indian, Chinese, and Mughal cuisines. The festival is a great way to enjoy a wide range of cuisine experiences and connect with other like-minded people.',
                    city_id=banglore.id,
                    details={'time': 'November 16-17, 2024', 'location': 'Jayamahal Palace, Bangalore'}
                ),
                Experience(
                    name='Echoes of Earth Music Festival',
                    type='local_event',
                    description='Echoes of Earth Music Festival is a free-to-attend cultural event that brings together musicians, dancers, and performers from across the country to perform live music and performances. The event is held annually in different cities across India, and is aimed at encouraging the cultural exchange and sharing of ideas between different cultures. The event is aimed at providing a platform for musicians to showcase their talents and to meet new people.',
                    city_id=banglore.id,
                    details={'time': 'November 23-24, 2024', 'location': 'Embassy International Riding School, Bangalore'}
                ),
                Experience(
                    name='Bangalore International Film Festival',
                    type='local_event',
                    description='Bangalore International Film Festival (BIFFES) is a 3-day event that brings together filmmakers, directors, and actors from around the world to showcase their work in the city. The event is held at various theatres across Bangalore, and features a wide range of films from various genres, including action, comedy, drama, and romance. The event is free to the public, and there are no entry fees.',
                    city_id=banglore.id,
                    details={'time': 'December 20-27, 2024', 'location': 'Various Theatres Across Bangalore'}
                ),
                Experience(
                    name='Christmas Carnival',
                    type='local_event',
                    description='Christmas Carnival is a popular festival in Bangalore that celebrates Christmas in the city. The festival is held on December 25th, and features a wide range of activities, including fireworks, games, and food. The event is free to the public, and there are no entry fees.',
                    city_id=banglore.id,
                    details={'time': 'December 24-25, 2024', 'location': 'St. Joseph’s College, Bangalore'}
                ),
                Experience(
                    name='Nrityagram',
                    type='walking_tour',
                    description='A unique dance village dedicated to the traditional Indian dance form of Odissi. It offers immersive experiences in dance and culture.',
                    city_id=banglore.id,
                    details={'type': 'Dance Village'}
                ),
                Experience(
                    name='Turahalli Forest',
                    type='walking_tour',
                    description='The last remaining forest in Bangalore, ideal for nature walks, cycling, and rock climbing. It features narrow trails and stunning viewpoints.',
                    city_id=banglore.id,
                    details={'type': 'Forest'}
                ),
                Experience(
                    name='Pyramid Valley',
                    type='walking_tour',
                    description='Hidden gem in Bangalore, a 1000-year-old pyramid-shaped structure that is a popular tourist attraction. It is located in the heart of the city and offers a unique view of the city skyline.',
                    city_id=banglore.id,
                    details={'type': 'Pyramid'}
                ),
                Experience(
                    name='Blossom Book House',
                    type='hidden_gem',
                    description='A charming second-hand bookstore filled with a wide range of books across genres. A haven for book lovers.',
                    city_id=banglore.id,
                    details={'type': 'Bookstore'}
                ),
                Experience(
                    name='Thindi Beedi',
                    type='hidden_gem',
                    description='A vibrant street food market offering a variety of local delicacies and snacks. Best visited in the evening.',
                    city_id=banglore.id,
                    details={'type': 'Food Street'}
                ) 
            ]
            db.session.add_all(experiences)
            db.session.commit()

if __name__ == '__main__':
    # Initialize the database first
    init_db()

    
    # Then run the app
    app = create_app()
    app.run()