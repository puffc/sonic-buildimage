/*****************************************************************
 *
 * DO NOT EDIT THIS FILE!
 * This file is auto-generated by xfc_map_parser
 * from the NPL output file(s) bcm56890_a0_cna_6_5_32_3_0_sf_match_id_info.yml
 * for device bcm56890_a0 and variant cna_6_5_32_3_0.
 * Edits to this file will be lost when it is regenerated.
 *
 * $Id: $
 * Copyright 2018-2024 Broadcom. All rights reserved.
 * The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License 
 * version 2 as published by the Free Software Foundation.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * A copy of the GNU General Public License version 2 (GPLv2) can
 * be found in the LICENSES folder.
 * All Rights Reserved.$
 *
 * Tool Path: $SDK/INTERNAL/fltg/xfc_map_parser
 *
 ****************************************************************/

#ifndef BCM56890_A0_CNA_6_5_32_3_0_BCMPKT_RXPMD_MATCH_ID_DEFS_H
#define BCM56890_A0_CNA_6_5_32_3_0_BCMPKT_RXPMD_MATCH_ID_DEFS_H

#include <bcmpkt/bcmpkt_rxpmd_match_id.h>

/*!
 * \brief Get the Match ID DataBase information.
 *
 * \retval bcmpkt_rxpmd_match_id_db_info_t Match ID DataBase information.
*/
extern bcmpkt_rxpmd_match_id_db_info_t *
    bcm56890_a0_cna_6_5_32_3_0_rxpmd_match_id_db_info_get(void);

/*!
 * \brief Get the Match ID Mapping information.
 *
 * \retval bcmpkt_rxpmd_match_id_map_info_t Match ID Mapping information.
*/
extern bcmpkt_rxpmd_match_id_map_info_t *
    bcm56890_a0_cna_6_5_32_3_0_rxpmd_match_id_map_info_get(void);

/*!
  \name RXPMD Match IDs
*/
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L2_HDR_ITAG  0
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L2_HDR_L2  1
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L2_HDR_NONE  2
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L2_HDR_OTAG  3
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_ARP  4
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_ETHERTYPE  5
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_ICMP  6
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_IPV4  7
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_IPV6  8
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_NONE  9
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_RARP  10
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_TCP_FIRST_4BYTES  11
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_TCP_LAST_16BYTES  12
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_UDP  13
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L3  14
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L4  15
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L5  16
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_VXLAN  17
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_SYS_HDR_EP_NIH  18
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_SYS_HDR_LOOPBACK  19
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_SYS_HDR_NONE  20
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L2_HDR_ITAG  21
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L2_HDR_L2  22
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L2_HDR_NONE  23
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L2_HDR_OTAG  24
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_ARP  25
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_ETHERTYPE  26
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_ICMP  27
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_IPV4  28
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_IPV6  29
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_NONE  30
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_RARP  31
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_TCP_FIRST_4BYTES  32
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_TCP_LAST_16BYTES  33
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_UDP  34
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L3  35
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L4  36
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L5  37
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_VXLAN  38
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L2_HDR_ITAG  39
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L2_HDR_L2  40
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L2_HDR_NONE  41
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L2_HDR_OTAG  42
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_ARP  43
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_ETHERTYPE  44
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_ICMP  45
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_IPV4  46
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_IPV6  47
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_NONE  48
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_RARP  49
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_TCP_FIRST_4BYTES  50
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_TCP_LAST_16BYTES  51
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_UDP  52
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L3  53
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L4  54
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L5  55
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L2_HDR_ITAG  56
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L2_HDR_L2  57
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L2_HDR_NONE  58
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L2_HDR_OTAG  59
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_ARP  60
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_ETHERTYPE  61
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_ICMP  62
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_IPV4  63
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_IPV6  64
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_NONE  65
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_RARP  66
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_TCP_FIRST_4BYTES  67
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_TCP_LAST_16BYTES  68
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_UDP  69
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L3  70
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L4  71
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L5  72
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_VXLAN  73
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_SYS_HDR_EP_NIH  74
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_SYS_HDR_LOOPBACK  75
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_SYS_HDR_NONE  76
#define BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_COUNT  77

#define BCM56890_A0_CNA_6_5_32_3_0_BCMPKT_RXPMD_MATCH_ID_FIELD_NAME_MAP_INIT \
    {"EGRESS_PKT_FWD_L2_HDR_ITAG", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L2_HDR_ITAG}, \
    {"EGRESS_PKT_FWD_L2_HDR_L2", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L2_HDR_L2}, \
    {"EGRESS_PKT_FWD_L2_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L2_HDR_NONE}, \
    {"EGRESS_PKT_FWD_L2_HDR_OTAG", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L2_HDR_OTAG}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_ARP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_ARP}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_ETHERTYPE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_ETHERTYPE}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_ICMP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_ICMP}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_IPV4", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_IPV4}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_IPV6", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_IPV6}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_NONE}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_RARP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_RARP}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_TCP_FIRST_4BYTES", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_TCP_FIRST_4BYTES}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_TCP_LAST_16BYTES", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_TCP_LAST_16BYTES}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_UDP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_UDP}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L3", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L3}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L4", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L4}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L5", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_UNKNOWN_L5}, \
    {"EGRESS_PKT_FWD_L3_L4_HDR_VXLAN", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_FWD_L3_L4_HDR_VXLAN}, \
    {"EGRESS_PKT_SYS_HDR_EP_NIH", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_SYS_HDR_EP_NIH}, \
    {"EGRESS_PKT_SYS_HDR_LOOPBACK", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_SYS_HDR_LOOPBACK}, \
    {"EGRESS_PKT_SYS_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_SYS_HDR_NONE}, \
    {"EGRESS_PKT_TUNNEL_L2_HDR_ITAG", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L2_HDR_ITAG}, \
    {"EGRESS_PKT_TUNNEL_L2_HDR_L2", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L2_HDR_L2}, \
    {"EGRESS_PKT_TUNNEL_L2_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L2_HDR_NONE}, \
    {"EGRESS_PKT_TUNNEL_L2_HDR_OTAG", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L2_HDR_OTAG}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_ARP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_ARP}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_ETHERTYPE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_ETHERTYPE}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_ICMP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_ICMP}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_IPV4", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_IPV4}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_IPV6", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_IPV6}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_NONE}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_RARP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_RARP}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_TCP_FIRST_4BYTES", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_TCP_FIRST_4BYTES}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_TCP_LAST_16BYTES", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_TCP_LAST_16BYTES}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_UDP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_UDP}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L3", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L3}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L4", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L4}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L5", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_UNKNOWN_L5}, \
    {"EGRESS_PKT_TUNNEL_L3_L4_HDR_VXLAN", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_EGRESS_PKT_TUNNEL_L3_L4_HDR_VXLAN}, \
    {"INGRESS_PKT_INNER_L2_HDR_ITAG", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L2_HDR_ITAG}, \
    {"INGRESS_PKT_INNER_L2_HDR_L2", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L2_HDR_L2}, \
    {"INGRESS_PKT_INNER_L2_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L2_HDR_NONE}, \
    {"INGRESS_PKT_INNER_L2_HDR_OTAG", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L2_HDR_OTAG}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_ARP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_ARP}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_ETHERTYPE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_ETHERTYPE}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_ICMP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_ICMP}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_IPV4", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_IPV4}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_IPV6", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_IPV6}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_NONE}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_RARP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_RARP}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_TCP_FIRST_4BYTES", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_TCP_FIRST_4BYTES}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_TCP_LAST_16BYTES", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_TCP_LAST_16BYTES}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_UDP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_UDP}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L3", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L3}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L4", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L4}, \
    {"INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L5", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_INNER_L3_L4_HDR_UNKNOWN_L5}, \
    {"INGRESS_PKT_OUTER_L2_HDR_ITAG", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L2_HDR_ITAG}, \
    {"INGRESS_PKT_OUTER_L2_HDR_L2", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L2_HDR_L2}, \
    {"INGRESS_PKT_OUTER_L2_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L2_HDR_NONE}, \
    {"INGRESS_PKT_OUTER_L2_HDR_OTAG", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L2_HDR_OTAG}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_ARP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_ARP}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_ETHERTYPE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_ETHERTYPE}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_ICMP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_ICMP}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_IPV4", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_IPV4}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_IPV6", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_IPV6}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_NONE}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_RARP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_RARP}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_TCP_FIRST_4BYTES", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_TCP_FIRST_4BYTES}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_TCP_LAST_16BYTES", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_TCP_LAST_16BYTES}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_UDP", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_UDP}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L3", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L3}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L4", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L4}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L5", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_UNKNOWN_L5}, \
    {"INGRESS_PKT_OUTER_L3_L4_HDR_VXLAN", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_OUTER_L3_L4_HDR_VXLAN}, \
    {"INGRESS_PKT_SYS_HDR_EP_NIH", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_SYS_HDR_EP_NIH}, \
    {"INGRESS_PKT_SYS_HDR_LOOPBACK", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_SYS_HDR_LOOPBACK}, \
    {"INGRESS_PKT_SYS_HDR_NONE", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_INGRESS_PKT_SYS_HDR_NONE}, \
    {"rxpmd_match_id_count", BCM56890_A0_CNA_6_5_32_3_0_RXPMD_MATCH_ID_COUNT}

#endif /*! BCM56890_A0_CNA_6_5_32_3_0_BCMPKT_RXPMD_MATCH_ID_DEFS_H */
