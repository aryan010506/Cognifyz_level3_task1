import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pandas as pd

def scrape_headlines():
    URL = "https://www.bbc.com/news"
    
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find headline elements
        headlines = soup.find_all('h3')
        filtered = [h.get_text(strip=True) for h in headlines if h.get_text(strip=True) != ""]
        titles = filtered[:10]

        if not titles:
            raise Exception("No headlines found. Website structure may have changed.")

        # Display in GUI
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "📰 Top BBC News Headlines:\n\n")
        for i, title in enumerate(titles, 1):
            output_box.insert(tk.END, f"{i}. {title}\n\n")

        # Save to CSV
        df = pd.DataFrame({'Headline': titles})
        df.to_csv('bbc_headlines.csv', index=False)
        messagebox.showinfo("Success", "Headlines saved to 'bbc_headlines.csv'")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# GUI Setup
app = tk.Tk()
app.title("News Headline Scraper")
app.geometry("500x500")
app.resizable(False, False)

tk.Label(app, text="Click the button to scrape top BBC news headlines", font=("Arial", 12)).pack(pady=10)
tk.Button(app, text="Scrape Headlines", command=scrape_headlines, font=("Arial", 11)).pack(pady=5)

output_box = scrolledtext.ScrolledText(app, wrap=tk.WORD, font=("Arial", 10))
output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

app.mainloop()
