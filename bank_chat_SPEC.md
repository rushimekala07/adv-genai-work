# bank_chat_spec

## purpose
A chat program where a customer asks a bank assistant questions
and sees what each answer cost us.

## user
A bank customer typing in a terminal window

## It must
- show the assistant's answer to each question.
- keep chatting until the user types "quit".
- Remember what the user said earlier in the same chat.
- show each answer's cost in rupees and total so far.

## It must not
- keep the secret key inside the code
- Answer questions unrelated to banking.

## Done when
1. I ask "what is a fixed deposit?"-> a short,sensible answer,
2. I type "My name is Ravi", then "what's my name?"->it answers "Ravi".
3. I ask three questions  -> the rupees total goes up after every answer,
4. i type "quit" -> the program ends.