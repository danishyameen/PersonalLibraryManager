import streamlit as st
import json
import os

# Constants
DATA_FILE = "library.json"
FIELDS = ["title", "author", "year", "genre", "read"]

# Set page configuration
st.set_page_config(
    page_title=" GIAIC Books Library Manager",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)


# Load data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = load_data()

# Sidebar navigation
# Updated sidebar section with app details
st.sidebar.title("📚 Library Manager")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation Menu", [
    "Add Book", 
    "View Books", 
    "Search Books", 
    "Edit Book", 
    "Delete Book", 
    "Statistics"
])

# Add app details to sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ About This App")
st.sidebar.markdown("""
**GIAIC Library Manager** helps you:
- 🗃️ Organize your book collection
- 📖 Track reading progress
- 📊 Analyze reading habits
- 🔍 Quickly find books
- 📚 Manage your digital library
""")

st.sidebar.markdown("---")
st.sidebar.subheader("✨ Key Features")
st.sidebar.markdown("""
- CRUD Operations
- Local Storage (JSON)
- Search Functionality
- Reading Statistics
- Responsive UI
- Persistent Data
""")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Technical Specs")
st.sidebar.markdown("""
- Built with Python 🐍
- Streamlit Framework
- Local JSON Storage
- Session State Management
- Open Source Code
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Version:** 1.1.0  \n**Developer:** Danish Yameen  \n**Last Updated:** 20 March 2025")


# Helper functions
def book_form(defaults=None, edit_mode=False):
    defaults = defaults or {}
    with st.form(key="book_form"):
        title = st.text_input("Title", value=defaults.get("title", ""))
        author = st.text_input("Author", value=defaults.get("author", ""))
        year = st.number_input("Publication Year", min_value=1800, max_value=2100, 
                             value=defaults.get("year", 2023))
        genre = st.text_input("Genre", value=defaults.get("genre", ""))
        read = st.checkbox("Read", value=defaults.get("read", False))
        
        if st.form_submit_button("Save Book" if edit_mode else "Add Book"):
            if title and author and genre:
                return {
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": read
                }
            else:
                st.error("Please fill in all required fields")
    return None

# Main content
st.title("📚 GIAIC Books Library Manager")

# Add Book Page
if page == "Add Book":
    st.header("Add New Book")
    new_book = book_form()
    if new_book:
        st.session_state.library.append(new_book)
        save_data(st.session_state.library)
        st.success("Book added successfully!")

# View All Books Page
elif page == "View Books":
    st.header("Your Library")
    if not st.session_state.library:
        st.info("No books in your library yet!")
    else:
        for i, book in enumerate(st.session_state.library, 1):
            with st.expander(f"{i}. {book['title']} by {book['author']}"):
                st.markdown(f"""
                - **Year**: {book['year']}
                - **Genre**: {book['genre']}
                - **Read**: {'✅' if book['read'] else '❌'}
                """)

# Search Books Page
elif page == "Search Books":
    st.header("Search Books")
    search_term = st.text_input("Search by title or author")
    if search_term:
        results = [
            book for book in st.session_state.library
            if search_term.lower() in book['title'].lower() or 
            search_term.lower() in book['author'].lower()
        ]
        if results:
            st.subheader(f"Found {len(results)} books:")
            for book in results:
                st.write(f"- **{book['title']}** by {book['author']} ({book['year']})")
        else:
            st.info("No matching books found")

# Edit Book Page
elif page == "Edit Book":
    st.header("Edit Book")
    if st.session_state.library:
        titles = [book['title'] for book in st.session_state.library]
        selected_title = st.selectbox("Select Book to Edit", titles)
        book_to_edit = next(b for b in st.session_state.library if b['title'] == selected_title)
        
        updated_book = book_form(book_to_edit, edit_mode=True)
        if updated_book:
            index = next(i for i, b in enumerate(st.session_state.library) 
                        if b['title'] == selected_title)
            st.session_state.library[index] = updated_book
            save_data(st.session_state.library)
            st.success("Book updated successfully!")
    else:
        st.info("No books available to edit")

# Delete Book Page
elif page == "Delete Book":
    st.header("Delete Book")
    if st.session_state.library:
        titles = [book['title'] for book in st.session_state.library]
        selected_title = st.selectbox("Select Book to Delete", titles)
        
        if st.button("Confirm Delete"):
            st.session_state.library = [b for b in st.session_state.library 
                                       if b['title'] != selected_title]
            save_data(st.session_state.library)
            st.success("Book deleted successfully!")
    else:
        st.info("No books available to delete")

# Statistics Page
elif page == "Statistics":
    st.header("Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for b in st.session_state.library if b['read'])
    
    col1, col2 = st.columns(2)
    col1.metric("Total Books", total_books)
    col2.metric("Read Books", f"{read_books} ({read_books/total_books:.1%})" 
              if total_books else "N/A")
    
    if total_books:
        genres = [b['genre'] for b in st.session_state.library]
        unique_genres = set(genres)
        st.subheader("Genre Distribution")
        for genre in unique_genres:
            count = genres.count(genre)
            st.write(f"- {genre}: {count} ({count/total_books:.1%})")

# Footer
st.markdown("---")
st.markdown("Made with by ❤️ Danish Yameen | Powered by Streamlit")