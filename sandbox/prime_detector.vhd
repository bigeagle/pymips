-- File: prime_detector.vhd
-- Generated by MyHDL 0.6
-- Date: Thu Oct 21 11:30:50 2010

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_06.all;

entity prime_detector is
    port (
        I: in unsigned(3 downto 0);
        O: out unsigned(0 downto 0)
    );
end entity prime_detector;

architecture MyHDL of prime_detector is


begin


PRIME_DETECTOR_LOGIC: process (I) is
begin
    case to_integer(I) is
        when 0 => O <= "0";
        when 1 => O <= "0";
        when 2 => O <= "1";
        when 3 => O <= "1";
        when 4 => O <= "0";
        when 5 => O <= "1";
        when 6 => O <= "0";
        when 7 => O <= "1";
        when 8 => O <= "0";
        when 9 => O <= "0";
        when 10 => O <= "0";
        when 11 => O <= "1";
        when 12 => O <= "0";
        when 13 => O <= "1";
        when 14 => O <= "0";
        when others => O <= "0";
    end case;
end process PRIME_DETECTOR_LOGIC;

end architecture MyHDL;