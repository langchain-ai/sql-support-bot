"""
Customer Support Bot using DeepAgents

A customer support chatbot for a music store that can:
1. Help customers find songs, albums, and artists in the catalog
2. Look up customer account information

Built with DeepAgents - the agent autonomously decides which tools to use.
"""

from dotenv import load_dotenv
import sqlite3
import requests
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from deepagents import create_deep_agent

# Load environment variables
load_dotenv()


# Database setup
def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )


engine = get_engine_for_chinook_db()
db = SQLDatabase(engine)


# Music-related tools
@tool
def get_albums_by_artist(artist: str):
    """Get albums by an artist."""
    return db.run(
        f"""
        SELECT Album.Title, Artist.Name
        FROM Album
        JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Artist.Name LIKE '%{artist}%';
        """,
        include_columns=True
    )


@tool
def get_tracks_by_artist(artist: str):
    """Get songs by an artist (or similar artists)."""
    return db.run(
        f"""
        SELECT Track.Name as SongName, Artist.Name as ArtistName
        FROM Album
        LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
        LEFT JOIN Track ON Track.AlbumId = Album.AlbumId
        WHERE Artist.Name LIKE '%{artist}%';
        """,
        include_columns=True
    )


@tool
def check_for_songs(song_title: str):
    """Check if a song exists by its name."""
    return db.run(
        f"""
        SELECT * FROM Track WHERE Name LIKE '%{song_title}%';
        """,
        include_columns=True
    )


# Customer-related tools
@tool
def get_customer_info(customer_id: int):
    """Look up customer info given their ID. ALWAYS make sure you have the customer ID before invoking this."""
    return db.run(f"SELECT * FROM Customer WHERE CustomerID = {customer_id};")


def create_agent():
    """
    Create a DeepAgent with all tools.
    The agent autonomously decides which tools to use based on the user's query.
    """
    system_prompt = """You are a helpful customer service representative for a music store.

You can help customers in two main ways:

1. **Music inquiries**: Help customers find information about songs, albums, and artists in our catalog.
   - Use get_albums_by_artist to find albums by a specific artist
   - Use get_tracks_by_artist to find songs by an artist
   - Use check_for_songs to search for songs by title
   - When searching, the tools may return similar matches if exact matches aren't found

2. **Account management**: Help customers access their account information.
   - Use get_customer_info to look up customer details (requires customer ID)
   - Always ask for the customer ID before invoking the tool

Be polite, helpful, and guide customers to provide any information you need (like customer ID) before calling tools."""

    agent = create_deep_agent(
        model=ChatOpenAI(model="gpt-4o", temperature=0),
        tools=[
            get_albums_by_artist,
            get_tracks_by_artist,
            check_for_songs,
            get_customer_info
        ],
        system_prompt=system_prompt
    )

    return agent


# Main entry point
if __name__ == "__main__":
    print("=== SQL Support Bot with DeepAgents ===\n")
    print("Initializing agent...\n")

    agent = create_agent()

    print("Agent ready! Type 'quit' to exit.\n")

    # Interactive loop
    conversation_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        conversation_history.append({"role": "user", "content": user_input})

        # Invoke the agent
        result = agent.invoke({"messages": conversation_history})

        # Extract the latest AI response
        if result and "messages" in result:
            ai_message = result["messages"][-1]
            ai_content = ai_message.content if hasattr(ai_message, 'content') else str(ai_message)

            print(f"\nAssistant: {ai_content}\n")

            # Add to conversation history
            conversation_history.append({"role": "assistant", "content": ai_content})
