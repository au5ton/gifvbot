require 'telegram/bot'
require 'dotenv'
Dotenv.load('.env')

FILE_SIZE_MINIMUM = 1 * (10**7) # 10 megabytes
FILE_SIZE_MAXIMUM = 1 * (10**8) # 100 megabytes

def in_range(size)
    if size < FILE_SIZE_MAXIMUM && size > FILE_SIZE_MINIMUM
        return true
    end
    return false
end

# Trap ^C
Signal.trap("INT") {
    puts "\nShutting down gracefully..."
    sleep 1
    exit
}

# Trap `Kill `
Signal.trap("TERM") {
    puts "\nShutting down gracefully..."
    sleep 1
    exit
}

print('Checking auth for bot... ');
Telegram::Bot::Client.run(ENV['TELEGRAM_BOT_TOKEN']) do |bot|
    bot_username = bot.api.get_me()["result"]["username"]
    print("#{bot_username} ✅\n")
    bot.listen do |message|
        #puts "doc: #{message.document}, class: #{message.document.class}"
        #puts "\tmime: #{message.document.mime_type}, size: #{message.document.file_size}"
        #puts "\tin_range: #{in_range(message.document.file_size)}"
        #puts "photo: #{message.photo}, class: #{message.photo.class}"

        if message.document.instance_of? Telegram::Bot::Types::Document
            puts "mime: #{message.document.mime_type}, size: #{message.document.file_size}"
            if message.document.mime_type == "image/gif"
                puts "we gotta gif"
                puts bot.api.get_file({"file_id" => message.document.file_id}) # doesn't account for ResponseErrors
            end
        else
            puts "that boy aint right"
        end


        case message.text
        when '/start'
            bot.api.send_message(chat_id: message.chat.id, text: "Hello, #{message.from.first_name}")
        when '/stop'
            bot.api.send_message(chat_id: message.chat.id, text: "Bye, #{message.from.first_name}")
        end
    end
end
