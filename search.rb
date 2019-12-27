require 'uri'
require 'open-uri'
require 'nokogiri'
require 'selenium-webdriver'
# Scraperクラスを定義
class Scraper
  # initializeで@prefix, @query, @search_urlを定義
  def initialize(prefix, query)
    @prefix = prefix
    @query = URI.escape(query.encode("utf-8"))
    @search_url = "https://www.bing.com/images/search?q=" + @query
  end

  def scrape_img

    # Seleniumの機能
    driver = Selenium::WebDriver.for :chrome
    driver.navigate.to(@search_url)

    # 合計10スクロールする
    10.times do 
      # 1スクロール分のビューを表示
      driver.find_elements(:class, 'iusc').last.location_once_scrolled_into_view
      # その中にあるiuscというクラスを持つやつを数える
        current_count = driver.find_elements(:class, 'iusc').length
        # スクレイピングするときのマナー。ちょっと待つ
        until current_count < driver.find_elements(:class, 'iusc').length
          sleep(3)
        end
      # スクレイピングするときのマナー。ちょっと待つ
      sleep(5)
    end
# エレメンツの中にiuscクラスを持つやつ探してぶち込む
    elements = driver.find_elements(:class, "iusc")
    @array = []
    elements.each do |element|
      # 正規表現
      @array << element.attribute("m").scan(/","murl\":"(.+)","turl":/)
    end
    # 配列平らに
    @array = @array.flatten!

    @url_array = []
    @array.each do |img|
      # @url_arrayの中にjpgかpngの文字列の部分をぶち込む
      if /\.(jpg|png)$/ =~ img.to_s
        @url_array << URI.escape(img.to_s.force_encoding("utf-8"))
      end
    end

    @url_array.each_with_index do |url, i|
      begin
        # jpg, pngを分ける
        if /\.(jpg)$/ =~ url
          filename = "#{@prefix}_#{i}.jpg"
        else
          filename = "#{@prefix}_#{i}.png"
        end
        p filename + " << " + url
        # dirなければ作成、
        dirname = "#{@prefix}_img"
        FileUtils.mkdir_p(dirname) unless FileTest.exist?(dirname)
        # filepathにファイルを書き込み
        filepath = dirname + "/" + filename
        open(filepath, "wb") do |f|
          open(url.encode("utf-8", invalid: :replace, undef: :replace)) do |data|
            sleep(2)
            f.write(data.read)
          end
        end
        p "できたよ"
      rescue
      p "無理でした"
      end
    end
    driver.quit
  end
end

if __FILE__ == $0
  keywords = {"yamada" => "山田孝之",
              "kubota" => "窪田正孝", 
              "sakurai" => "櫻井翔", 
              "kurokawa" => "クロちゃん", 
              "matsumoto" => "松本人志", 
              "abe" => "阿部寛"
  }
  keywords.each do |prefix, query|
    p prefix
    p query
    scraper = Scraper.new(prefix, query)
    scraper.scrape_img
  end
end