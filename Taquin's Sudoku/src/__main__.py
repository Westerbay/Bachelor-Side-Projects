import os



if __name__ == "__main__":
    os.chdir("..")
    import interface.Interface as game
    game.Interface().run()
    
