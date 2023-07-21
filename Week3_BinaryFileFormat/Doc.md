# ඞ Amogus Matrix File ඞ

The File consists of headers, made up of 2 parts:

1. the headers name, ascii encoded string ended with Nullbyte \0
2. the headers content in a format defined <a href="#headers">below</a>

## Headers ඞ

-   ### date_i_fucked_your_mom:
    date of creation as 64-bit unix timestamp
-   ### motherfucker:
    srting; the files creator (who happened to be in your mother's room last night), ended by Nullbyte
-   ### data:

    must be the last header in the file

    binary containing an integer indicating the byte size of a single stored unit, an integer indicating the dimension count n followed by n integers containing the dimensions of the matrix, directly followed by the flattened matrix

## File Extension ඞ

Please use the file extension ".amongus" or you will be indentified as the Imposter (ඞ sus)
