from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string('''
<CustomLayout>
    canvas.before:
        Color:
            rgba: 0, 1, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size
<RootWidget>
    CustomLayout:
        AsyncImage:
            source: 'http://www.everythingzoomer.com/wp-content/uploads/2013/01/Monday-joke-289x277.jpg'
            size_hint: 1, .5
            pos_hint: {'center_x':.5, 'center_y': .5}
    AsyncImage:
        source: 'http://www.stuffistumbledupon.com/wp-content/uploads/2012/05/Have-you-seen-this-dog-because-its-awesome-meme-puppy-doggy.jpg'
    CustomLayout
        AsyncImage:
            source: 'http://www.stuffistumbledupon.com/wp-content/uploads/2012/04/Get-a-Girlfriend-Meme-empty-wallet.jpg'
            size_hint: 1, .5
            pos_hint: {'center_x':.5, 'center_y': .5}
''')


class RootWidget(BoxLayout):
    pass


class CustomLayout(FloatLayout):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':

    MainApp().run()