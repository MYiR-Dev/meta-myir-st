import re
import subprocess
import chardet
import json
VERSION_RGX = re.compile("version\s+\d+", re.IGNORECASE)
class Iwlist_Parse:

    def __init__(self):
        pass
    def get_name(self,cell):
        """ Gets the name / essid of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The name / essid of the network.
        """

        essid = self.matching_line(cell, "ESSID:")
        if not essid:
            return ""
        # s=essid.encode('raw_unicode_escape')
        # print s
        # ss= s.decode('utf8')
        #
        # print ss

        return essid[1:-1]

    def get_quality(self,cell):
        """ Gets the quality of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The quality of the network.
        """

        quality = self.matching_line(cell, "Quality=")
        if quality is None:
            return ""
        quality = quality.split()[0].split("/")
        quality = self.matching_line(cell, "Quality=").split()[0].split("/")
        return str(int(round(float(quality[0]) / float(quality[1]) * 100)))

    def get_signal_level(self,cell):
        """ Gets the signal level of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The signal level of the network.
        """

        signal = self.matching_line(cell, "Signal level=")
        if signal is None:
          return ""
        signal = signal.split("=")[1].split("/")
        if len(signal) == 2:
            return str(int(round(float(signal[0]) / float(signal[1]) * 100)))
        elif len(signal) == 1:
            return signal[0].split(' ')[0]
        else:
            return ""

    def get_noise_level(self,cell):
        """ Gets the noise level of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The noise level of the network.
        """

        noise = self.matching_line(cell, "Noise level=")
        if noise is None:
            return ""
        noise = noise.split("=")[1]
        return noise.split(' ')[0]

    def get_channel(self,cell):
        """ Gets the channel of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The channel of the network.
        """

        channel = self.matching_line(cell, "Channel:")
        if channel:
            return channel
        frequency = self.matching_line(cell, "Frequency:")
        channel = re.sub(r".*\(Channel\s(\d{1,3})\).*", r"\1", frequency)
        return channel

    def get_frequency(self,cell):
        """ Gets the frequency of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The frequency of the network.
        """

        frequency = self.matching_line(cell, "Frequency:")
        if frequency is None:
            return ""
        return frequency.split()[0]

    def get_encryption(self,cell, emit_version=False):
        """ Gets the encryption type of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The encryption type of the network.
        """

        enc = ""
        if self.matching_line(cell, "Encryption key:") == "off":
            enc = "Open"
        else:
            for line in cell:
                matching = self.match(line,"IE:")
                if matching == None:
                    continue

                wpa = self.match(matching,"WPA")
                if wpa == None:
                    continue

                version_matches = VERSION_RGX.search(wpa)
                if len(version_matches.regs) == 1:
                    version = version_matches \
                        .group(0) \
                        .lower() \
                        .replace("version", "") \
                        .strip()
                    wpa = wpa.replace(version_matches.group(0), "").strip()
                    if wpa == "":
                        wpa = "WPA"
                    if emit_version:
                        enc = "{0} v.{1}".format(wpa, version)
                    else:
                        enc = wpa
                    if wpa == "WPA2":
                        return enc
                else:
                    enc = wpa
            if enc == "":
                enc = "WEP"
        return enc

    def get_mode(self,cell):
        """ Gets the mode of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The IEEE 802.11 mode of the network.
        """

        mode = self.matching_line(cell, "Extra:ieee_mode=")
        if mode is None:
            return ""
        return mode

    def get_address(self,cell):
        """ Gets the address of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The address of the network.
        """

        return self.matching_line(cell, "Address: ")

    def get_bit_rates(self,cell):
        """ Gets the bit rate of a network / cell.
        @param string cell
            A network / cell from iwlist scan.
        @return string
            The bit rate of the network.
        """

        return self.matching_line(cell, "Bit Rates:")

    # Here you can choose the way of sorting the table. sortby should be a key of
    # the dictionary rules.

    def sort_cells(self,cells):
        sortby = "Quality"
        reverse = True
        cells.sort(key=lambda el:el[sortby], reverse=reverse)


    # Below here goes the boring stuff. You shouldn't have to edit anything below
    # this point

    def matching_line(self, lines, keyword):
        """ Returns the first matching line in a list of lines.
        @see match()
        """
        for line in lines:
            matching = self.match(line,keyword)
            if matching != None:
                return matching
        return None

    def match(self, line, keyword):
        """ If the first part of line (modulo blanks) matches keyword,
        returns the end of that line. Otherwise checks if keyword is
        anywhere in the line and returns that section, else returns None"""

        line = line.lstrip()
        length = len(keyword)
        if line[:length] == keyword:
            return line[length:]
        else:
            if keyword in line:
                return line[line.index(keyword):]
            else:
                return None

    def parse_cell(self, cell, rules):
        """ Applies the rules to the bunch of text describing a cell.
        @param string cell
            A network / cell from iwlist scan.
        @param dictionary rules
            A dictionary of parse rules.
        @return dictionary
            parsed networks. """

        parsed_cell = {}
        for key in rules:
            rule = rules[key]
            parsed_cell.update({key: rule(cell)})
        return parsed_cell

    def print_table(self, table):
        # Functional black magic.
        widths = list(map(max, map(lambda l: map(len, l), zip(*table))))

        justified_table = []
        for line in table:
            justified_line = []
            for i, el in enumerate(line):
                justified_line.append(el.ljust(widths[i] + 2))
            justified_table.append(justified_line)

        for line in justified_table:
            print("\t".join(line))

    def print_cells(self , cells, columns):
        table = [columns]
        for cell in cells:
            cell_properties = []
            for column in columns:
                if column == 'Quality':
                    # make print nicer
                    cell[column] = cell[column].rjust(3) + " %"
                cell_properties.append(cell[column])
            table.append(cell_properties)
        self.print_table(table)

    def get_parsed_cells(self, iw_data, rules=None):
        """ Parses iwlist output into a list of networks.
            @param list iw_data
                Output from iwlist scan.
                A list of strings.
            @return list
                properties: Name, Address, Quality, Channel, Frequency, Encryption, Signal Level, Noise Level, Bit Rates, Mode.
        """

        # Here's a dictionary of rules that will be applied to the description
        # of each cell. The key will be the name of the column in the table.
        # The value is a function defined above.
        rules = rules or {
            "Name": self.get_name,
            "Quality": self.get_quality,
            "Channel":  self.get_channel,
            "Frequency":  self.get_frequency,
            "Encryption":  self.get_encryption,
            "Address":  self.get_address,
            "Signal Level":  self.get_signal_level,
            "Noise Level":  self.get_noise_level,
            "Bit Rates":  self.get_bit_rates,
            "Mode":  self.get_mode,
        }

        cells = [[]]
        parsed_cells = []

        for line in iw_data:
            cell_line = self.match(line, "Cell ")
            if cell_line != None:
                cells.append([])
                line = cell_line[-27:]
            cells[-1].append(line.rstrip())

        cells = cells[1:]

        for cell in cells:
            parsed_cells.append(self.parse_cell(cell, rules))

        self.sort_cells(parsed_cells)
        return parsed_cells

    def call_iwlist(self, interface):
        """ Get iwlist output via subprocess
            @param string interface
                interface to scan
                default is wlan0
            @return string
                properties: iwlist output
        """
        return subprocess.check_output(['iwlist', interface, 'scanning'])

    def get_interfaces(self,interface):
        """ Get parsed iwlist output
            @param string interface
                interface to scan
                default is wlan0
            @param list columns
                default data attributes to return
            @return dict
                properties: dictionary of iwlist attributes
        """
        return self.get_parsed_cells(self.call_iwlist(interface).split('\n'))