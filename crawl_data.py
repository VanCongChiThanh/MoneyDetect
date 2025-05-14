from bing_image_downloader import downloader

downloader.download("5 euro banknote front", 
                    limit=30, 
                    output_dir='data', 
                    adult_filter_off=True, 
                    force_replace=False, 
                    timeout=60)
