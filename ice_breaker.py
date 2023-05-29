from rich import print
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from output_parsers import person_intel_parser, PersonIntel


def ice_breaker(name: str) -> PersonIntel:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url,
        data_file="./data/proxycurl-2023-05-29T18:03:47.005077.json",
    )

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(
        twitter_username,
        num_tweets=10,
        data_file="./data/dataset_twitter-scraper_2023-05-29_17-56-33-862.json",
    )

    summary_template = """ given the Linkedin information
    {linkedin_information} and twitter {twitter_information} about a person
    from I want you to create:
    1. a short summary
    2. two interesting facts about them
    3. A topic that may interest them
    4. 2 creative ice breakers toopen a conversation with them
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions(),
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(
        linkedin_information=linkedin_data, twitter_information=tweets
    )
    print(result)
    return person_intel_parser.parse(result)


if __name__ == "__main__":
    print("Hello LangChain!")
    ice_breaker(name="Rod Morison")
