# 📝 network

Welcome to the **Network Project**! This web application lets users post updates, follow others, and engage with posts by liking and editing them. The project is built using **Python**, **JavaScript**, **HTML**, and **CSS** to deliver a seamless social networking experience. Let's dive in! 🌐🚀  

---

## 💡 Features  

1. **New Post 🖊️**  
   - Users can write text-based posts.
   - Posts are submitted through a text area and appear on the site immediately.  

2. **All Posts 📃**  
   - View all posts from all users in **reverse chronological order** (newest first).
   - Each post displays the **username**, **content**, **timestamp**, and **like count**.  

3. **User Profile Pages 👤**  
   - Displays the number of **followers** and **following**.
   - Shows the user’s posts in **reverse chronological order**.
   - Users can **follow/unfollow** other users from their profile page.
   - **Self-following is not allowed.**  

4. **Following Page 👥**  
   - Shows posts from users that the logged-in user follows.
   - Only available to **signed-in users**.

5. **Pagination ⏭️⏮️**  
   - Pages display **10 posts per page**.
   - Navigate using **Next** and **Previous** buttons for a smooth browsing experience.

6. **Edit Post ✏️**  
   - Users can **edit their own posts** via an **Edit** button.
   - Changes are saved without reloading the page, using **JavaScript and fetch API** for a smooth user experience.
   - Users cannot edit other users' posts (security enforced!).  

7. **Like/Unlike Posts ❤️👎**  
   - Toggle likes on any post in real-time.
   - Like count updates **asynchronously** via JavaScript fetch, without a page reload.

---

## 🛠️ Tech Stack  

- **Backend**: Python with Flask or Django  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: SQLite (or any SQL-based DB)  
- **AJAX**: JavaScript fetch API for real-time interactions  

---

## 🚀 How to Run  

1. **Clone the repository**:  
   ```bash
   git clone git@github.com:chiragsingla014/network.git
   cd network
   ```
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Migrate Database**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Run the App**:
    ```bash
    python manage.py runserver
    ```

5. Visit `http://127.0.0.1:8000` in your web browser to access the app.



## 🧑‍💻 Usage Instructions  

1. **Sign up / Log in** to start posting!  
2. Create a **New Post** by typing in the textarea and submitting it.  
3. Browse **All Posts** from all users or visit the **Following** page to see posts from people you follow.  
4. Visit **user profiles** by clicking on usernames.  
5. **Follow or unfollow** users to customize your feed.  
6. Click the **like button** to engage with posts you love!  
7. Edit your posts by clicking the **Edit button** and save changes without refreshing.

---

## 🔐 Security Measures  

- Users **cannot edit posts made by others**.  
- **Self-following** is disabled to prevent circular following.  
- AJAX calls handle **likes and edits asynchronously** for better performance and UX.

---

## ✨ Future Improvements  

- Add **commenting functionality** for better post interaction.  
- Implement **real-time notifications** for likes and follows.  
- Add support for **image-based posts** to make posts more engaging.  

---

## 🤝 Contributions  

Contributions are welcome! If you would like to contribute, feel free to open an issue or a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.