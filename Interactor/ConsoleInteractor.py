from Interactor.Interactor import Interactor


class ConsoleInteractor(Interactor):

    def send_message(self, text: str):
        self._chat.send_text(text)

    def receive_message(self) -> str:
        data = self._chat.receive_text()

        return data

    def interaction_loop(self):
        should_continue = True

        if self._chat.is_server:
            print(f'Client: {self.receive_message()}')

        while should_continue:
            text = input('You: ')

            if text == 'exit':
                should_continue = False
                continue

            self._chat.send_text(text)
            response = self.receive_message()
            print(f'Client: {response}')

