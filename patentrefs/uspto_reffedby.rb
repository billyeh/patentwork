#!/usr/bin/env ruby

require 'nokogiri'
require 'json'
require 'csv'
require 'open-uri'

class USPTOFetcher

  def initialize(argv)
    begin
      patentpage = Nokogiri::HTML(open("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2Fsearch-adv.htm&r=0&f=S&l=50&d=PALL&Query=ref/#{argv}"))
    rescue OpenURI::HTTPError
      patentpage = "link broken"
    end
    outFile = File.new("./uspto_refs/#{argv}.html", "a+")
    outFile.puts(patentpage)
    outFile.close
  end

end

puts 'Checking for data from USPTO...'
if not File.directory?("./uspto_refs")
  Dir.mkdir('./uspto_refs')
end

CSV.foreach("clean_200_random.csv") do |patent|
  if not File.file?("./uspto_refs/" + patent[0] + ".html")
    puts patent[0]
    scrape = USPTOFetcher.new(patent[0])
  end
end

class USPTOScraper

  def initialize(patent)
    # URL for search on patent number defined above
    patentpage = Nokogiri::HTML(open("./uspto_refs/#{patent}.html"))

    doc = patentpage.xpath("//body/table")
    rows = doc.xpath("//table//tr[1 <= position() and position() < 200]/td[2]/a/text()")

    @uspto_refs_list = Array.new
    rows.each do |r|
      @uspto_refs_list.push("0" + r.to_s.gsub(/,/,''))
    end

    def uspto_refs_list
      @uspto_refs_list
    end
  end

end

uspto_ref_hash = Hash.new

puts 'These patents may have more than 50 refs, check USPTO website'
CSV.foreach("clean_200_random.csv") do |patent|
  ref = USPTOScraper.new(patent[0])
  uspto_ref_hash[patent[0]] = ref.uspto_refs_list.reverse
  if ref.uspto_refs_list.length >= 50
    puts patent[0]
  end
end

File.open('uspto_ref_hash.json', 'w+') do |f|
  f.write(JSON.pretty_generate(uspto_ref_hash))
end

puts 'Done!'
