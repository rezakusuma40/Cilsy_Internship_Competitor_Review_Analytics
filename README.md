## Project Relevance and Context

During my internship at Cilsy Fiolution, the task at hand was to initiate a data engineering project tailored for immediate applicability within the company's infrastructure. Given the absence of significant big data engineering implementations, I sought to fill this void by conceptualizing a text exploration initiative focusing on app reviews for comprehensive market research.

The decision to embark on this project stemmed from a strategic evaluation of the company's ongoing endeavors. At that juncture, Cilsy Fiolution was in the developmental phase of a project management app named Cicle. As this application was relatively new in the market, the development team was actively seeking strategies to bolster its traction, enhance feature competitiveness, and address prevailing bugs. Recognizing the pivotal role of user reviews in shaping product development, I undertook the exploration of competitors' app reviews with the specific intent of furnishing the development team with nuanced insights and actionable intelligence.

This project aligned seamlessly with the company's objectives, aiming to equip the development team with a more comprehensive understanding of the competitive landscape and user expectations.

### Approach and Methodology

While this project could be executed using personal computing resources, I chose to leverage the capabilities of the Google Cloud Platform (GCP) due to its superior availability, security, and fault tolerance.

- Data Collection and Cleansing: Utilizing Python, I initiated the project by scraping the Google Play Store and App Store for user reviews. Subsequently, I cleansed the acquired data to ensure its quality and reliability.
- GCP Tools Utilization: Leveraging Google Compute Engine, I executed the scripts, storing raw data in Google Cloud Storage as a robust data lake and depositing clean data into Google BigQuery, serving as the project's data warehouse.
- Data Loading and Processing: I orchestrated the transfer of data from BigQuery to Elastic Cloud using Google DataFlow, crafting an efficient and streamlined pipeline for seamless data management.
- Cost Optimization: Part of the project scope included minimizing costs. To achieve this, I employed the GCP Calculator, ensuring cost-efficiency in project execution.

### Data Collection and Source Limitations

The initial phase involved scraping user reviews from a diverse array of 14 competitor apps available on the Google Play Store and App Store. Notably, these apps included Slack, Trello, Asana, Microsoft Teams, Basecamp, Monday.com, Jira Cloud, Wrike, Smartsheet, Zoho Projects, Quire, Todoist, Meistertask, and Proofhub. Unfortunately, accessing reviews from other platforms was restricted due to protective measures, rendering any attempts illegal. Moreover, encountering API request limitations on the App Store capped the scraping capacity at 2000 reviews per app. Despite these hurdles, the data amassed from the Google Play Store yielded a substantial pool of 233,330 user reviews.

Notably, the decision to omit scraping Cicle reviews stemmed from the app's limited review count at that time. Considering the sparse availability of reviews, implementing a robust data engineering approach for Cicle seemed unnecessary. However, I established an adaptable ETL (Extract, Transform, Load) pipeline during this project, envisioning its applicability for future data collection encompassing Cicle reviews.

### Data Exploration and Insights

Delving into the amassed data provided invaluable insights:

- Rating Distribution and Feature Analysis: Analyzing recent reviews, I extracted the rating distribution for each app within the last 90 days. Further analysis involved comparing ratings for specific features, such as notifications, to ascertain their impact on overall ratings.
- Text Filtering and Elasticsearch Utilization: Utilizing Elasticsearch's robust text search capabilities, I filtered reviews pertinent to specific topics by employing targeted word searches. This approach aided in pinpointing relevant data amidst the textual chaos.
- Insights and Recommendations: Notably, I discovered that reviews regarding notification features across all apps predominantly held a 1-star rating. These findings demand further exploration to identify underlying issues and strategize on leveraging this information to gain a competitive edge.
- Visualization and Reporting: To encapsulate and present the project's findings comprehensively, I created a comprehensive report utilizing Kibana's visualization capabilities.

This repository encapsulates the core pipeline, insights, and report derived from this comprehensive data engineering endeavor, laying a foundation for data-informed strategies at Cilsy Fiolution.

### Further Exploration and Future Implementation

While conducting this project, I encountered limitations attempting to explore Elasticsearch locally due to installation issues on my personal system. Subsequently, I utilized Elastic Cloud, albeit at a considerable cost for personal usage. As the primary objective of this task was to present a data engineering project applicable within the company rather than to actively utilize the obtained results, I opted to forgo extensive exploration at that stage. However, the meticulously designed data pipeline and scripts I developed stand as a valuable resource that Cilsy can seamlessly employ for future exploration.

Notably, although this project does not currently integrate machine learning functionalities, the meticulously cleansed dataset presented herein stands primed for future machine learning tasks. This dataset exhibits readiness for various machine learning applications, such as Natural Language Processing (NLP), text classification, and text mining.

Please note that due to file size constraints (exceeding 25MB), I regret that I couldn't upload the dataset along with this repository.
