/*
 *  nextpnr -- Next Generation Place and Route
 *
 *  Copyright (C) 2018  Clifford Wolf <clifford@clifford.at>
 *
 *  Permission to use, copy, modify, and/or distribute this software for any
 *  purpose with or without fee is hereby granted, provided that the above
 *  copyright notice and this permission notice appear in all copies.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 *  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 *  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 *  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 *  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 *  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 *  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 */

#include <math.h>
#include "nextpnr.h"

NEXTPNR_NAMESPACE_BEGIN

Arch::Arch(ArchArgs) {}

std::string Arch::getChipName() { return "Dummy"; }

void IdString::initialize_arch(Context *ctx) {}

// ---------------------------------------------------------------

BelId Arch::getBelByName(IdString name) const { return BelId(); }

IdString Arch::getBelName(BelId bel) const { return IdString(); }

void Arch::bindBel(BelId bel, IdString cell) {}

void Arch::unbindBel(BelId bel) {}

bool Arch::checkBelAvail(BelId bel) const { return false; }

IdString Arch::getBelCell(BelId bel, bool conflicting) const
{
    return IdString();
}

const std::vector<BelId> &Arch::getBels() const
{
    static std::vector<BelId> ret;
    return ret;
}

const std::vector<BelId> &Arch::getBelsByType(BelType type) const
{
    static std::vector<BelId> ret;
    return ret;
}

BelType Arch::getBelType(BelId bel) const { return BelType(); }

WireId Arch::getWireBelPin(BelId bel, PortPin pin) const { return WireId(); }

BelPin Arch::getBelPinUphill(WireId wire) const { return BelPin(); }

const std::vector<BelPin> &Arch::getBelPinsDownhill(WireId wire) const
{
    static std::vector<BelPin> ret;
    return ret;
}

// ---------------------------------------------------------------

WireId Arch::getWireByName(IdString name) const { return WireId(); }

IdString Arch::getWireName(WireId wire) const { return IdString(); }

void Arch::bindWire(WireId wire, IdString net) {}

void Arch::unbindWire(WireId wire) {}

bool Arch::checkWireAvail(WireId wire) const { return false; }

IdString Arch::getWireNet(WireId wire, bool conflicting) const
{
    return IdString();
}

const std::vector<WireId> &Arch::getWires() const
{
    static std::vector<WireId> ret;
    return ret;
}

// ---------------------------------------------------------------

PipId Arch::getPipByName(IdString name) const { return PipId(); }

IdString Arch::getPipName(PipId pip) const { return IdString(); }

void Arch::bindPip(PipId pip, IdString net) {}

void Arch::unbindPip(PipId pip) {}

bool Arch::checkPipAvail(PipId pip) const { return false; }

IdString Arch::getPipNet(PipId pip, bool conflicting) const
{
    return IdString();
}

const std::vector<PipId> &Arch::getPips() const
{
    static std::vector<PipId> ret;
    return ret;
}

WireId Arch::getPipSrcWire(PipId pip) const { return WireId(); }

WireId Arch::getPipDstWire(PipId pip) const { return WireId(); }

DelayInfo Arch::getPipDelay(PipId pip) const { return DelayInfo(); }

const std::vector<PipId> &Arch::getPipsDownhill(WireId wire) const
{
    static std::vector<PipId> ret;
    return ret;
}

const std::vector<PipId> &Arch::getPipsUphill(WireId wire) const
{
    static std::vector<PipId> ret;
    return ret;
}

const std::vector<PipId> &Arch::getWireAliases(WireId wire) const
{
    static std::vector<PipId> ret;
    return ret;
}

// ---------------------------------------------------------------

bool Arch::estimatePosition(BelId bel, int &x, int &y) const
{
    x = 0.0;
    y = 0.0;
    return false;
}

delay_t Arch::estimateDelay(WireId src, WireId dst) const { return 0.0; }

// ---------------------------------------------------------------

std::vector<GraphicElement> Arch::getFrameGraphics() const
{
    static std::vector<GraphicElement> ret;
    return ret;
}

std::vector<GraphicElement> Arch::getBelGraphics(BelId bel) const
{
    static std::vector<GraphicElement> ret;
    return ret;
}

std::vector<GraphicElement> Arch::getWireGraphics(WireId wire) const
{
    static std::vector<GraphicElement> ret;
    return ret;
}

std::vector<GraphicElement> Arch::getPipGraphics(PipId pip) const
{
    static std::vector<GraphicElement> ret;
    return ret;
}

NEXTPNR_NAMESPACE_END