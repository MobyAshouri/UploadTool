import customtkinter as ctk
import instagrapi
import json
from PIL import ImageTk, Image

def main():

    def showLoginInfo(platform):

        def saveAndLogIn(platform, username, password):
            try:
                with open("gui/logins.json", "r") as file:
                    info = json.load(file)

                info[platform]["Username"] = username
                info[platform]["Password"] = password

                with open("gui/logins.json", "w") as file:
                    json.dump(info, file, indent=3)

            except:
                toplevel = ctk.CTkToplevel()
                toplevel.resizable(False, False)
                toplevel.title("Error")
                label = ctk.CTkLabel(toplevel, text="Could not save login information\ngui/logins.json might not be able to be found")
                label.pack(padx=20, pady=20)


            try:
                cl = instagrapi.Client()
                cl.login(username=username, password=password)

                try:
                    with open("gui/logins.json", "r") as file:
                        info = json.load(file)

                    info[platform]["LoggedIn?"] = True

                    with open("gui/logins.json", "w") as file:
                        json.dump(info, file, indent=3)
                except:
                    toplevel = ctk.CTkToplevel()
                    toplevel.resizable(False, False)
                    label = ctk.CTkLabel(toplevel, text="Could not save that user's login attempt was successful")
                    label.pack(padx=20, pady=20)

                toplevel = ctk.CTkToplevel()
                toplevel.resizable(False, False)
                label = ctk.CTkLabel(toplevel, text=f"Logged in successfully to {platform}")
                toplevel.title("Successfully logged in")
                label.pack(padx=20, pady=20)

            except:
                toplevel = ctk.CTkToplevel()
                toplevel.resizable(False, False)
                toplevel.title("Error")
                label = ctk.CTkLabel(toplevel, text="Incorrect log in")
                label.pack(padx=20, pady=20)

        loginWindow = ctk.CTkToplevel()
        loginWindow.resizable(False, False)
        loginWindow.geometry("400x125")

        loginWindow.title("Log in")

        builtFrame = ctk.CTkFrame(loginWindow)
        userNameFrame = ctk.CTkFrame(builtFrame, width=300, corner_radius=0)
        passWordFrame = ctk.CTkFrame(builtFrame, width=300, corner_radius=0)
        
        loginWindow.grid_rowconfigure(0, weight=1)
        loginWindow.grid_rowconfigure(1, weight=1)
        loginWindow.grid_columnconfigure(0, weight=1)
        loginWindow.grid_columnconfigure(1, weight=1)

        with open("gui/logins.json", "r") as file:
            info = json.load(file)


        userNameEntry = ctk.CTkEntry(userNameFrame, corner_radius=5, width=250, placeholder_text=f"{info[platform]['Username']}")
        passWordEntry = ctk.CTkEntry(passWordFrame, corner_radius=5, width=250, placeholder_text=f"{info[platform]['Password']}")

        userNameLabel = ctk.CTkLabel(userNameFrame, text="Username: ")
        passWordLabel = ctk.CTkLabel(passWordFrame, text="Password: ")

        userNameLabel.grid(row=0, column=0, padx=20, pady=10, sticky="nesw")
        userNameEntry.grid(row=0, column=1, padx=20, pady=10, sticky="nesw")
        passWordLabel.grid(row=0, column=0, padx=20, pady=10, sticky="nesw")
        passWordEntry.grid(row=0, column=1, padx=20, pady=10, sticky="nesw")

        userNameFrame.grid(row=0, column=0, sticky="ew")
        passWordFrame.grid(row=1, column=0, sticky="ew")

        submitButton = ctk.CTkButton(builtFrame, text="Log In", fg_color="darkred", hover_color="red", command=lambda: saveAndLogIn(platform=platform, username=userNameEntry.get(), password=passWordEntry.get()))
        submitButton.grid(row=2, column=0, sticky="ew")

        builtFrame.pack()


    def buildUploadWindow():
        StartButton.destroy()
        win.update()
        win.geometry("870x420")

        imagePaths = {"instagram": "media/images/instagramLogo.png",
                      "tiktok": "media/images/tiktokLogo.png",
                      "youtube": "media/images/youtubeLogo.png"}
        
        image = Image.open(imagePaths['instagram']).resize((200,200))
        image = ImageTk.PhotoImage(image=image)
        ImageLabel = ctk.CTkButton(win, text="", image=image, fg_color="white", hover_color="darkred", corner_radius=50, command=lambda: showLoginInfo("Instagram"))
        ImageLabel.grid(row=0, column=0, padx=20, pady=20)

        image = Image.open(imagePaths['tiktok']).resize((200,200))
        image = ImageTk.PhotoImage(image=image)
        ImageLabel = ctk.CTkButton(win, text="", image=image, fg_color="white", hover_color="darkred", corner_radius=50, command=lambda: showLoginInfo("TikTok"))
        ImageLabel.grid(row=0, column=1, padx=20, pady=20)

        image = Image.open(imagePaths['youtube']).resize((200,200))
        image = ImageTk.PhotoImage(image=image)
        ImageLabel = ctk.CTkButton(win, text="", image=image, fg_color="white", hover_color="darkred", corner_radius=50, command=lambda: showLoginInfo("YouTube"))
        ImageLabel.grid(row=0, column=2, padx=20, pady=20)

        ig_checkButton = ctk.CTkCheckBox(win, text="Instagram?")
        ig_checkButton.grid(row=1, column=0)

        tt_checkbuttons = ctk.CTkCheckBox(win, text="TikTok?")
        tt_checkbuttons.grid(row=1, column=1)

        yt_checkButton = ctk.CTkCheckBox(win, text="YouTube?")
        yt_checkButton.grid(row=1, column=2)

        filePathLabel = ctk.CTkLabel(win, text="No File Currently Selected")
        def openFile():
            filePath = ctk.filedialog.askopenfilename()
            filePathLabel.configure(text=filePath)

        buttonFrame = ctk.CTkFrame(win)

        selectFileButton = ctk.CTkButton(buttonFrame, text="Select a file", fg_color="darkred", hover_color="red", command=openFile)
        selectFileButton.grid(row=0, column=0, padx=5)

        def checkLoginStatus():
            with open("gui/logins.json", "r") as file:
                info = json.load(file)

            string = ""

            if info["Instagram"]["LoggedIn?"]:
                string+="Instagram: ✅"
            else:
                string+="Instagram: ❌"
            string+="\n"

            if info["TikTok"]["LoggedIn?"]:
                string+="TikTok: ✅"
            else:
                string+="TikTok: ❌"
            string+="\n"

            if info["YouTube"]["LoggedIn?"]:
                string+="YouTube: ✅"
            else:
                string+="YouTube: ❌"
            string+="\n"

            statusChecker = ctk.CTkToplevel()
            statusChecker.resizable(False, False)
            statusChecker.title("Checking Status...")
            statusChecker.geometry("200x80")
            statusLabel = ctk.CTkLabel(statusChecker, text=string)
            statusLabel.pack(pady=10, padx=10)

        loginStatus = ctk.CTkButton(buttonFrame, text="Check saved log in status", fg_color="darkred", hover_color="red", command=checkLoginStatus)
        loginStatus.grid(row=0, column=1, padx=5)

        buttonFrame.grid(row=2, column=1, pady=20)

        filePathLabel.grid(row=3, column=0, columnspan=3)

        def uploadVideo():
            with open("gui/logins.json", "r") as file:
                info = json.load(file)

            if ig_checkButton.get():
                cl = instagrapi.Client()
                cl.login(info["Instagram"]["Username"], info["Instagram"]["Password"])
                cl.clip_upload(filePathLabel.cget("text"), caption=captionEntry.get())

            if yt_checkButton.get():
                pass
            if tt_checkbuttons.get():
                pass

        uploadFrame = ctk.CTkFrame(win)
        captionEntry = ctk.CTkEntry(uploadFrame, text_color="white", width=600, placeholder_text="Caption...")
        captionEntry.grid(row=0, column=0, padx=10, pady=10)

        uploadButton = ctk.CTkButton(uploadFrame, text="Upload", fg_color="darkred", hover_color="red", command=uploadVideo)
        uploadButton.grid(row=0, column=1, pady=10)

        uploadFrame.grid(row=4, column=0, columnspan=3)
        

    win = ctk.CTk()
    win.geometry("600x400")
    win.title("Incarnate Editors Upload Tool")
    win.resizable(False, False)

    StartButton = ctk.CTkButton(win, text="Upload a Reel", command=buildUploadWindow)
    StartButton.pack()

    win.mainloop()

    

main()