#!/usr/bin/env ruby

require 'nokogiri'
require 'open-uri'
require 'csv'
require 'json'

class GoogleFetcher

  def initialize(argv)
    begin
      patentpage = Nokogiri::HTML(open("http://www.google.com/patents/US#{argv}"))
    rescue OpenURI::HTTPErrors
      patentpage = "link broken"
    end
    outFile = File.new("./google_refs/#{argv}.html", "a+")
    outFile.puts(patentpage)
    outFile.close
  end

end

puts 'Checking for data from Google...'
if not File.directory?("./google_refs")
  Dir.mkdir('./google_refs')
end

CSV.foreach("clean_200_random.csv") do |patent|
  if not File.file?("./google_refs/" + patent[0] + ".html")
    puts patent[0]
    scrape = GoogleFetcher.new(patent[0])
  end
end

class GoogleScraper

  def initialize(patent) # default patent
    patentpage = Nokogiri::HTML(open("./google_refs/#{patent}.html"))

    @google_refs_list = Array.new
    patentpage.css('td.patent-data-table-td > a').each do |node|
      if node.parent.parent.parent.parent.text.match(/^\nReferenced by/)
        @google_refs_list.push(node.text)
      end
    end
  end

  def google_refs_list
    @google_refs_list
  end

end

google_ref_hash = Hash.new

CSV.foreach("clean_200_random.csv") do |patent|
  google_ref_hash[patent[0]] = GoogleScraper.new(patent[0]).google_refs_list.reverse
end

File.open('google_ref_hash.json', 'w+') do |f|
  f.write(JSON.pretty_generate(google_ref_hash))
end

puts 'Done!'