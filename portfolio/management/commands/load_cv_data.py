from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import Profile
from portfolio.models import Experience, Skill, Project


class Command(BaseCommand):
    help = "Load CV data into the database"

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create or update profile
            try:
                from django.contrib.auth import get_user_model

                User = get_user_model()
                user = User.objects.get(id=1)  # Assuming user with ID 1

                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={
                        "title": "Backend Developer",
                        "profession_titles": [
                            "Junior Backend Developer",
                            "Backend Developer",
                        ],
                        "phone": "+9862170984",
                        "experience_years": 1,
                        "about_short": "Junior Backend Developer with Django and Python expertise",
                        "about_detailed": "Junior Backend Developer with a solid foundation in Python and Django. Experienced in building RESTful APIs using Django REST Framework (DRF) and working with relational databases. Strong understanding of backend development principles, including authentication, data modeling, and API integration. Enthusiastic about learning new technologies and contributing to real-world projects in a collaborative team environment.",
                        "skills_summary": "Python, Django, Django Rest Framework, API Development",
                        "preferred_work_type": "full_time",
                    },
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        "User with ID 1 not found. Please create a user first."
                    )
                )
                return

            # Create skills
            skills_data = [
                {
                    "name": "Python",
                    "level": "expert",
                    "percentage": 95,
                    "icon_class": "fab fa-python",
                },
                {
                    "name": "Django",
                    "level": "expert",
                    "percentage": 90,
                    "icon_class": "fas fa-code",
                },
                {
                    "name": "Django Rest Framework",
                    "level": "expert",
                    "percentage": 85,
                    "icon_class": "fas fa-code",
                },
                {
                    "name": "Django Celery",
                    "level": "advanced",
                    "percentage": 75,
                    "icon_class": "fas fa-cogs",
                },
                {
                    "name": "GitHub",
                    "level": "expert",
                    "percentage": 90,
                    "icon_class": "fab fa-github",
                },
                {
                    "name": "JavaScript",
                    "level": "intermediate",
                    "percentage": 70,
                    "icon_class": "fab fa-js",
                },
                {
                    "name": "SQL",
                    "level": "intermediate",
                    "percentage": 65,
                    "icon_class": "fas fa-database",
                },
                {
                    "name": "FastAPI",
                    "level": "beginner",
                    "percentage": 40,
                    "icon_class": "fas fa-bolt",
                },
            ]

            for skill_data in skills_data:
                skill, created = Skill.objects.get_or_create(
                    name=skill_data["name"],
                    defaults={
                        "level": skill_data["level"],
                        "percentage": skill_data["percentage"],
                        "icon_class": skill_data["icon_class"],
                        "is_featured": skill_data["percentage"] >= 80,
                        "order": 0,
                    },
                )
                if created:
                    self.stdout.write(f"Created skill: {skill.name}")

            # Create experiences
            experiences_data = [
                {
                    "company": "The Big Solutions",
                    "position": "Junior Backend Developer",
                    "location": "Bhaktapur, Nepal",
                    "start_date": "2025-04-01",
                    "is_current": True,
                    "employment_type": "full_time",
                    "description": "Developed and optimized scalable APIs using DRF, improving API response time. Automated 100+ PDF ticket distributions with Django Celery and WeasyPrint. Implemented digital signature validation middleware for secure partner API interactions. Contributed to 5 major projects: Event & Voting, Marketplace, and Insurance Premium Calculator, Koshi Premier League (Ecommerce), Shree Om Mandir.",
                    "achievements": [
                        "Developed RESTful APIs for secure voting system",
                        "Automated PDF ticket generation with WeasyPrint",
                        "Implemented digital signature validation",
                        "Contributed to 5+ major projects",
                    ],
                },
                {
                    "company": "The Big Solutions",
                    "position": "Intern",
                    "location": "Bhaktapur, Nepal",
                    "start_date": "2024-12-01",
                    "end_date": "2025-04-01",
                    "is_current": False,
                    "employment_type": "internship",
                    "description": "Gained hands-on experience in web application development with Python, Django, and Django Rest Framework. Assisted in various stages of project development, enhancing foundational coding and framework skills.",
                    "achievements": [
                        "Learned Django and DRF",
                        "Assisted in project development",
                        "Enhanced coding skills",
                    ],
                },
            ]

            for exp_data in experiences_data:
                experience, created = Experience.objects.get_or_create(
                    company=exp_data["company"],
                    position=exp_data["position"],
                    defaults={
                        "location": exp_data["location"],
                        "start_date": exp_data["start_date"],
                        "end_date": exp_data.get("end_date"),
                        "is_current": exp_data["is_current"],
                        "employment_type": exp_data["employment_type"],
                        "description": exp_data["description"],
                        "achievements": exp_data["achievements"],
                        "order": 0,
                    },
                )

                # Add technologies to experience
                if created:
                    # Add relevant skills to each experience
                    if (
                        "Backend" in exp_data["position"]
                        or "API" in exp_data["description"]
                    ):
                        python_skill = Skill.objects.get(name="Python")
                        django_skill = Skill.objects.get(name="Django")
                        drf_skill = Skill.objects.get(name="Django Rest Framework")
                        experience.technologies.add(
                            python_skill, django_skill, drf_skill
                        )

                if created:
                    self.stdout.write(
                        f"Created experience: {exp_data['position']} at {exp_data['company']}"
                    )

            # Create social links
            social_links_data = [
                {
                    "platform": "github",
                    "url": "https://github.com/451suman",
                    "icon_class": "fab fa-github",
                },
                {
                    "platform": "linkedin",
                    "url": "https://linkedin.com/in/suman-mushyakhwo-200088219",
                    "icon_class": "fab fa-linkedin",
                },
                {
                    "platform": "website",
                    "url": "https://sumanmushyakhwo.com.np/",
                    "icon_class": "fas fa-globe",
                },
            ]

            for link_data in social_links_data:
                try:
                    social_link, created = SocialLink.objects.get_or_create(
                        profile=profile,
                        platform=link_data["platform"],
                        defaults={
                            "url": link_data["url"],
                            "icon_class": link_data["icon_class"],
                            "is_active": True,
                            "order": 0,
                        },
                    )
                    if created:
                        self.stdout.write(
                            f"Created social link: {link_data['platform']}"
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error creating social link {link_data['platform']}: {e}"
                        )
                    )

            # Create sample projects
            projects_data = [
                {
                    "title": "Event and Voting System",
                    "slug": "event-voting-system",
                    "description": "Developed RESTful APIs for a secure voting system, enabling users to vote on their favorite contestants in competitions such as singing, dancing, or modeling through client-side and partner-side applications. Built admin panel APIs to create events, manage voting options, monitor results, and control the voting workflow. Implemented dynamic registration forms to collect participant and voter information efficiently. Designed event ticketing APIs for concerts, sports, and other events, integrating Celery to handle bulk ticket generation and WeasyPrint to generate PDF tickets. Automated email distribution of tickets to event participants, improving operational efficiency and user experience.",
                    "short_description": "Secure voting system with event management and ticketing",
                    "status": "completed",
                    "is_featured": True,
                    "github_url": "https://github.com/451suman/event-voting",
                    "live_url": "https://example.com/event-voting",
                    "start_date": "2025-01-01",
                    "end_date": "2025-03-01",
                    "duration_weeks": 8,
                    "team_size": 3,
                    "technologies": [
                        "Python",
                        "Django",
                        "Django Rest Framework",
                        "Django Celery",
                        "WeasyPrint",
                    ],
                },
                {
                    "title": "Koshi Premier League (E-commerce & Live Score System)",
                    "slug": "koshi-premier-league",
                    "description": "Developed RESTful APIs for a platform combining e-commerce functionality with live match score display for the Koshi Premier League. Built and maintained admin-side APIs for managing products, orders, and e-commerce operations. Implemented client-facing APIs used by the frontend to display products, match information, and live scores. Integrated Celery for background task processing to improve system performance and reliability.",
                    "short_description": "E-commerce platform with live scoring system",
                    "status": "completed",
                    "is_featured": True,
                    "github_url": "https://github.com/451suman/koshi-premier-league",
                    "live_url": "https://koshi-premier-league.com",
                    "start_date": "2025-02-01",
                    "end_date": "2025-05-01",
                    "duration_weeks": 17,
                    "team_size": 4,
                    "technologies": [
                        "Python",
                        "Django",
                        "Django Rest Framework",
                        "Celery",
                    ],
                },
                {
                    "title": "Marketplace Platform",
                    "slug": "marketplace-platform",
                    "description": "Developed and maintained RESTful APIs for a multi-merchant marketplace platform. Implemented a merchant system where merchants can add products and manage product variants. Designed architecture where multiple merchant websites use the same backend APIs but have different frontend implementations. Built partner integration APIs allowing partners to consume marketplace APIs and display products on their own portals. Implemented order management and settlement logic based on merchant-specific transactions. Ensured API performance, security, and maintainability across multiple clients and partner integrations.",
                    "short_description": "Multi-merchant marketplace with partner integrations",
                    "status": "completed",
                    "is_featured": False,
                    "github_url": "https://github.com/451suman/marketplace",
                    "live_url": "https://example.com/marketplace",
                    "start_date": "2025-03-01",
                    "end_date": "2025-06-01",
                    "duration_weeks": 13,
                    "team_size": 5,
                    "technologies": ["Python", "Django", "Django Rest Framework"],
                },
                {
                    "title": "Premium Insurance Calculator",
                    "slug": "premium-insurance-calculator",
                    "description": "Developed a premium calculation system for Rastriya Jeevan Beema to help users compare multiple insurance plans. Implemented backend logic to calculate insurance premiums based on policy duration, payment terms, and selected plans. Integrated features for comparing benefits such as Premium Waiver and Accidental Death coverage. Designed accurate calculation formulas to ensure reliable premium estimates and faster decision-making for users.",
                    "short_description": "Insurance premium comparison calculator",
                    "status": "completed",
                    "is_featured": False,
                    "github_url": "https://github.com/451suman/insurance-calculator",
                    "live_url": "https://example.com/insurance-calculator",
                    "start_date": "2025-04-01",
                    "end_date": "2025-05-01",
                    "duration_weeks": 4,
                    "team_size": 2,
                    "technologies": ["Python", "Django", "Django Rest Framework"],
                },
                {
                    "title": "Blue Book Renewal System",
                    "slug": "blue-book-renewal",
                    "description": "Implemented partner models for third-party integrations. Developed robust backend logic for validating digital signatures against request body content. Integrated this validation logic into a custom middleware to secure processing external API requests. Built an Admin Panel using Django Templates for managing partners and system data efficiently.",
                    "short_description": "Partner integration system with digital signature validation",
                    "status": "completed",
                    "is_featured": False,
                    "github_url": "https://github.com/451suman/blue-book-renewal",
                    "live_url": "https://example.com/blue-book-renewal",
                    "start_date": "2025-05-01",
                    "end_date": "2025-06-01",
                    "duration_weeks": 4,
                    "team_size": 3,
                    "technologies": ["Python", "Django", "Django Rest Framework"],
                },
            ]

            for project_data in projects_data:
                project, created = Project.objects.get_or_create(
                    title=project_data["title"],
                    defaults={
                        "slug": project_data["slug"],
                        "description": project_data["description"],
                        "short_description": project_data["short_description"],
                        "status": project_data["status"],
                        "is_featured": project_data["is_featured"],
                        "is_open_source": True,
                        "github_url": project_data["github_url"],
                        "live_url": project_data["live_url"],
                        "start_date": project_data["start_date"],
                        "end_date": project_data["end_date"],
                        "duration_weeks": project_data["duration_weeks"],
                        "team_size": project_data["team_size"],
                        "challenges": "Overcame tight deadlines and complex business logic requirements while ensuring code quality and maintainability.",
                        "architecture": "Built scalable microservices architecture with proper separation of concerns, implemented comprehensive error handling and logging, and followed Django best practices for security and performance.",
                    },
                )

                # Add technologies to project
                if created:
                    for tech_name in project_data["technologies"]:
                        try:
                            tech = Skill.objects.get(name=tech_name)
                            project.technologies.add(tech)
                        except Skill.DoesNotExist:
                            self.stdout.write(
                                f"Skill '{tech_name}' not found, skipping..."
                            )

                if created:
                    self.stdout.write(f"Created project: {project_data['title']}")

            self.stdout.write(self.style.SUCCESS("CV data loaded successfully!"))
